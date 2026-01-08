"""Add user profile fields

Revision ID: 006
Revises: 005
Create Date: 2026-01-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('debug_mode', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('language', sa.String(), nullable=False, server_default='pt-BR'))
    op.add_column('users', sa.Column('notifications', sa.Boolean(), nullable=False, server_default='true'))

def downgrade() -> None:
    op.drop_column('users', 'notifications')
    op.drop_column('users', 'language')
    op.drop_column('users', 'debug_mode')
    op.drop_column('users', 'name')
