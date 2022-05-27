"""add content

Revision ID: 9c02fd7c5b3d
Revises: 5dd18a74d5b9
Create Date: 2022-05-26 14:35:58.600486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c02fd7c5b3d'
down_revision = '5dd18a74d5b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
