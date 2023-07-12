"""deleted_at, external update

Revision ID: a7cacac45f60
Revises: d06dcd5dad76
Create Date: 2023-07-11 19:55:30.388178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a7cacac45f60'
down_revision = 'd06dcd5dad76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('categories', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('chat_tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('chats', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('chats', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('messages', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('messages', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_chats', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('users', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('users', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('users', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_chats', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('messages', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('messages', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('chats', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('chats', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('chat_tags', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('categories', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('categories', 'external',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)
    # ### end Alembic commands ###
