"""Add last edited audit fields to sales

Revision ID: c9d8e7f6a5b4
Revises: b53c6a7d8e9f
Create Date: 2026-06-01 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9d8e7f6a5b4"
down_revision: Union[str, Sequence[str], None] = "b53c6a7d8e9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sales", sa.Column("last_edited_by", sa.String(), nullable=True))
    op.add_column("sales", sa.Column("last_edited_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("sales", "last_edited_at")
    op.drop_column("sales", "last_edited_by")
