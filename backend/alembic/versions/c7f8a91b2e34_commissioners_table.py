"""Commissioners table

Revision ID: c7f8a91b2e34
Revises: efecfc98d10e
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c7f8a91b2e34'
down_revision: Union[str, Sequence[str], None] = 'efecfc98d10e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'commissioners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('commissioner_group_id', sa.Integer(), nullable=True),
        sa.Column('role', sa.String(), server_default='commissioner', nullable=False),
        sa.Column('full_access', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
    )
    op.create_index(op.f('ix_commissioners_id'), 'commissioners', ['id'], unique=False)
    op.create_index(op.f('ix_commissioners_username'), 'commissioners', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_commissioners_username'), table_name='commissioners')
    op.drop_index(op.f('ix_commissioners_id'), table_name='commissioners')
    op.drop_table('commissioners')
