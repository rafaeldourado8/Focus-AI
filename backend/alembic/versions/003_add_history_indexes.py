"""add history indexes

Revision ID: 003
Revises: 002
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona índices para melhorar performance de queries de histórico
    op.create_index('idx_questions_session_created', 'questions', ['session_id', 'created_at'])
    op.create_index('idx_answers_question', 'answers', ['question_id'])
    op.create_index('idx_sessions_user_created', 'learning_sessions', ['user_id', 'created_at'])


def downgrade():
    op.drop_index('idx_sessions_user_created', table_name='learning_sessions')
    op.drop_index('idx_answers_question', table_name='answers')
    op.drop_index('idx_questions_session_created', table_name='questions')
