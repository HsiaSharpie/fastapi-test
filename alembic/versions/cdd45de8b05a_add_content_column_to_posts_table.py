"""add content column to posts table

Revision ID: cdd45de8b05a
Revises: 1a816f358e50
Create Date: 2022-06-02 11:11:27.876273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cdd45de8b05a"
down_revision = "1a816f358e50"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
