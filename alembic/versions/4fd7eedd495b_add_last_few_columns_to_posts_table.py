"""add last few columns to posts table

Revision ID: 4fd7eedd495b
Revises: 41b92ec86674
Create Date: 2022-06-02 15:58:49.147796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4fd7eedd495b"
down_revision = "41b92ec86674"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
