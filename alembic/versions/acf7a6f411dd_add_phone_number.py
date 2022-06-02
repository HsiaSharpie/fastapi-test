"""add phone number

Revision ID: acf7a6f411dd
Revises: 459cef279929
Create Date: 2022-06-02 16:19:14.443668

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "acf7a6f411dd"
down_revision = "459cef279929"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_column("users", "phone_number")
    pass
