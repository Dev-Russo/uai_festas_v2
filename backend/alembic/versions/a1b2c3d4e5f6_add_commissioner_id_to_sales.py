"""Add commissioner_id to sales

Revision ID: a1b2c3d4e5f6
Revises: d4e5f6a7b8c9
Create Date: 2026-04-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sales', sa.Column('commissioner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_sales_commissioner_id',
        'sales', 'commissioners',
        ['commissioner_id'], ['id'],
    )


def downgrade() -> None:
    op.drop_constraint('fk_sales_commissioner_id', 'sales', type_='foreignkey')
    op.drop_column('sales', 'commissioner_id')
