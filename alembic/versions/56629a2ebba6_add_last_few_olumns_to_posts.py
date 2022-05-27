"""add last few olumns to posts

Revision ID: 56629a2ebba6
Revises: a432cc0f2301
Create Date: 2022-05-26 16:16:15.114457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56629a2ebba6'
down_revision = 'a432cc0f2301'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
