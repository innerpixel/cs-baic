"""pgvector cosine top-K retrieval helper."""
from dataclasses import dataclass
from typing import Optional
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class ChunkHit:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    filename: str
    content: str
    score: float


def top_k(
    db: Session,
    query_embedding: list[float],
    k: int = 5,
    exclude_document_ids: Optional[list[uuid.UUID]] = None,
) -> list[ChunkHit]:
    """Return top-K chunks by cosine similarity to query_embedding."""
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    exclude_clause = ""
    params: dict = {"embedding": embedding_str, "k": k}

    if exclude_document_ids:
        placeholders = ", ".join(f":excl_{i}" for i in range(len(exclude_document_ids)))
        exclude_clause = f"AND dc.document_id NOT IN ({placeholders})"
        for i, doc_id in enumerate(exclude_document_ids):
            params[f"excl_{i}"] = str(doc_id)

    sql = text(f"""
        SELECT
            dc.id          AS chunk_id,
            dc.document_id,
            d.filename,
            dc.content,
            1 - (dc.embedding <=> CAST(:embedding AS vector)) AS score
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        WHERE dc.embedding IS NOT NULL
        {exclude_clause}
        ORDER BY dc.embedding <=> CAST(:embedding AS vector)
        LIMIT :k
    """)

    rows = db.execute(sql, params).fetchall()
    return [
        ChunkHit(
            chunk_id=row.chunk_id,
            document_id=row.document_id,
            filename=row.filename,
            content=row.content,
            score=float(row.score),
        )
        for row in rows
    ]
