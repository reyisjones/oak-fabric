import json

from src.common.storage import database
from src.embeddings.client import ModelClient, ModelError


def search(question: str, model: ModelClient, top_k: int = 5, min_score: float = 0.35) -> list[dict]:
    if not question.strip() or not 1 <= top_k <= 5 or not 0 <= min_score <= 1:
        raise ValueError("Invalid search query, top_k, or minimum score")
    vector = json.dumps(model.embed([question], query=True)[0])
    with database() as conn:
        config = conn.execute("SELECT model, dimensions FROM embedding_config WHERE singleton").fetchone()
        if config != (model.embedding_model, 768):
            raise ModelError("Embedding configuration differs from index")
        rows = conn.execute(
            """SELECT c.chunk_id, c.entry_id, c.text, c.metadata,
                      1 - (c.embedding <=> %s::vector) AS score
               FROM chunks c JOIN documents d ON d.id = c.entry_id
               WHERE d.status = 'approved'
               ORDER BY c.embedding <=> %s::vector, c.chunk_id LIMIT %s""",
            (vector, vector, top_k),
        ).fetchall()
    return [{"chunk_id": r[0], "entry_id": r[1], "text": r[2], "metadata": r[3], "score": r[4]}
            for r in rows if r[4] is not None and r[4] >= min_score]
