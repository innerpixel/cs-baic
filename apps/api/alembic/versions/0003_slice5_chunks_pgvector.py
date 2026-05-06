"""slice-5 chunks + pgvector

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-06

Requires: pgvector/pgvector:pg16 docker image (or postgresql-16-pgvector apt package).
Run: cd infra && docker compose down && docker compose up -d postgres
Then: uv run alembic upgrade head
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

# Match EMBEDDING_DIMENSIONS in .env (default 1024 for mistral-embed)
VECTOR_DIM = 1024


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "document_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", sa.Text(), nullable=True),  # placeholder; replaced below
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
        ),
    )

    # Replace text placeholder with proper VECTOR type
    op.execute(f"ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector({VECTOR_DIM}) USING NULL")

    # HNSW index for cosine similarity (preferred over ivfflat — no train step required)
    op.execute(
        "CREATE INDEX document_chunks_embedding_idx "
        "ON document_chunks USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.drop_table("document_chunks")
    op.execute("DROP EXTENSION IF EXISTS vector")
