"""add feedback table

Revision ID: 005
Revises: 004
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa

revision = '005'
down_revision = '004'
depends_on = None

def upgrade():
    op.create_table(
        'answer_feedback',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('answer_id', sa.String(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_feedback_answer_id'), 'answer_feedback', ['answer_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_answer_feedback_answer_id'), table_name='answer_feedback')
    op.drop_table('answer_feedback')
