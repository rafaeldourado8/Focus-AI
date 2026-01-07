"""Add activation fields

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.String(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('activation_code', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'activation_code')
    op.drop_column('users', 'is_active')
