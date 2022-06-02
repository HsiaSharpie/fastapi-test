"""auto-vote

Revision ID: 459cef279929
Revises: 4fd7eedd495b
Create Date: 2022-06-02 16:09:36.402982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "459cef279929"
down_revision = "4fd7eedd495b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    pass


def downgrade():
    op.drop_table("votes")
    pass
