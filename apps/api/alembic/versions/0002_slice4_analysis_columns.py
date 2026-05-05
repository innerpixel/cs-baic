"""slice-4 analysis columns

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("document_analyses", sa.Column("detected_type", sa.String(64), nullable=True))
    op.add_column("document_analyses", sa.Column("confidence", sa.Float, nullable=True))
    op.add_column("document_analyses", sa.Column("language", sa.String(16), nullable=True))
    op.add_column("document_analyses", sa.Column("urgency", sa.String(16), nullable=True))
    op.add_column("document_analyses", sa.Column("analyzer_outputs", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("document_analyses", "analyzer_outputs")
    op.drop_column("document_analyses", "urgency")
    op.drop_column("document_analyses", "language")
    op.drop_column("document_analyses", "confidence")
    op.drop_column("document_analyses", "detected_type")
