"""Add buyer_cpf and sale_type to sales

Revision ID: b53c6a7d8e9f
Revises: a1b2c3d4e5f6
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b53c6a7d8e9f'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sales', sa.Column('buyer_cpf', sa.String(), nullable=True))
    op.add_column('sales', sa.Column('sale_type', sa.String(), nullable=True))

    op.execute("UPDATE sales SET buyer_cpf = '' WHERE buyer_cpf IS NULL")
    op.execute("UPDATE sales SET sale_type = 'regular' WHERE sale_type IS NULL")

    op.alter_column('sales', 'buyer_cpf', nullable=False)
    op.alter_column('sales', 'sale_type', nullable=False, server_default='regular')


def downgrade() -> None:
    op.drop_column('sales', 'sale_type')
    op.drop_column('sales', 'buyer_cpf')
