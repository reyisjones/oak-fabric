import hashlib
import json
from dataclasses import dataclass

from src.extraction.documents import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    source_type: str
    title: str
    section: str
    page: int | None
    image_reference: str | None
    created_at: str
    technology: tuple[str, ...]
    architecture: tuple[str, ...]
    tags: tuple[str, ...]
    text: str


def chunk_document(document: Document, size: int = 1200, overlap: int = 150) -> list[Chunk]:
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    chunks = []
    for section_index, section in enumerate(document.sections):
        start = 0
        while start < len(section.text):
            end = min(start + size, len(section.text))
            identity = json.dumps([document.document_id, document.source, section_index, start, end])
            chunks.append(Chunk(
                chunk_id=hashlib.sha256(identity.encode()).hexdigest(),
                document_id=document.document_id,
                source=document.source,
                source_type=document.source_type,
                title=document.title,
                section=section.section,
                page=section.page,
                image_reference=None,
                created_at=document.created_at,
                technology=(), architecture=(), tags=(),
                text=section.text[start:end],
            ))
            if end == len(section.text):
                break
            start = end - overlap
    return chunks
