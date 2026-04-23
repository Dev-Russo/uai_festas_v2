"""Product groups and memberships

Revision ID: d4e5f6a7b8c9
Revises: c7f8a91b2e34
Create Date: 2026-04-21 00:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c7f8a91b2e34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('parent_group_id', sa.Integer(), nullable=True),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.ForeignKeyConstraint(['parent_group_id'], ['product_groups.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_product_groups_id'), 'product_groups', ['id'], unique=False)

    op.create_table(
        'product_group_memberships',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['product_groups.id']),
        sa.ForeignKeyConstraint(['product_id'], ['product.id']),
        sa.PrimaryKeyConstraint('product_id', 'group_id'),
    )


def downgrade() -> None:
    op.drop_table('product_group_memberships')
    op.drop_index(op.f('ix_product_groups_id'), table_name='product_groups')
    op.drop_table('product_groups')
