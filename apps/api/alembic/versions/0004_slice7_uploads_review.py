"""slice-7 dev_source · review_state · batch_id · pdf_path

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-11
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "documents",
        sa.Column(
            "source",
            sa.String(32),
            nullable=True,
            server_default="public",
        ),
    )
    op.add_column(
        "documents",
        sa.Column(
            "review_state",
            sa.String(32),
            nullable=True,
            server_default="pending",
        ),
    )
    op.add_column(
        "documents",
        sa.Column("review_note", sa.Text(), nullable=True),
    )
    op.add_column(
        "documents",
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "documents",
        sa.Column("pdf_path", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("documents", "pdf_path")
    op.drop_column("documents", "batch_id")
    op.drop_column("documents", "review_note")
    op.drop_column("documents", "review_state")
    op.drop_column("documents", "source")
