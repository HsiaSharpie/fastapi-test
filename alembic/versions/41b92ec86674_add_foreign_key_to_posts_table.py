"""add foreign-key to posts table

Revision ID: 41b92ec86674
Revises: 4f01e47f5002
Create Date: 2022-06-02 15:37:12.181477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41b92ec86674"
down_revision = "4f01e47f5002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
