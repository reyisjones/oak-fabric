import hashlib
import json
from dataclasses import asdict

from psycopg.types.json import Jsonb

from src.chunking.text import chunk_document
from src.common.storage import database, preserve_source
from src.embeddings.client import ModelClient, ModelError
from src.extraction.documents import extract_document

MAX_CHUNKS = 100


def ingest(source: str, content: bytes, model: ModelClient) -> dict:
    document = extract_document(source, content)
    chunks = chunk_document(document)
    if len(chunks) > MAX_CHUNKS:
        raise ValueError("Document exceeds the initial 100-chunk ingestion limit")
    entry_id = hashlib.sha256(json.dumps([source, document.document_id]).encode()).hexdigest()
    with database() as conn:
        config = conn.execute("SELECT model, dimensions FROM embedding_config WHERE singleton").fetchone()
        if config != (model.embedding_model, 768):
            raise ModelError("Embedding configuration differs from index; rebuild in a separate index before switching models")
        existing = conn.execute("SELECT status FROM documents WHERE id = %s", (entry_id,)).fetchone()
        if existing:
            return {"id": entry_id, "document_id": document.document_id, "chunks": len(chunks), "status": existing[0], "created": False}
    object_key = preserve_source(document.document_id, content)
    vectors = []
    for start in range(0, len(chunks), 8):
        vectors.extend(model.embed([chunk.text for chunk in chunks[start:start + 8]]))
    with database() as conn:
        inserted = conn.execute(
            "INSERT INTO documents (id, document_id, source, source_type, title, object_key) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id",
            (entry_id, document.document_id, source, document.source_type, document.title, object_key),
        ).fetchone()
        if inserted:
            with conn.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO chunks (chunk_id, entry_id, text, metadata, embedding) VALUES (%s,%s,%s,%s,%s::vector)",
                    [(c.chunk_id, entry_id, c.text, Jsonb({k: v for k, v in asdict(c).items() if k != "text"}), json.dumps(v)) for c, v in zip(chunks, vectors, strict=True)],
                )
        status = conn.execute("SELECT status FROM documents WHERE id = %s", (entry_id,)).fetchone()[0]
    return {"id": entry_id, "document_id": document.document_id, "chunks": len(chunks), "status": status, "created": bool(inserted)}


def approve(entry_id: str) -> bool:
    with database() as conn:
        record = conn.execute("SELECT source FROM documents WHERE id = %s", (entry_id,)).fetchone()
        if record is None:
            return False
        # Serialize publication of revisions sharing a source, including concurrent approvals.
        conn.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))", (record[0],))
        conn.execute("UPDATE documents SET status = 'superseded' WHERE source = %s AND status = 'approved' AND id <> %s", (record[0], entry_id))
        conn.execute("UPDATE documents SET status = 'approved' WHERE id = %s", (entry_id,))
    return True
