"""add columns

Revision ID: 92c9a9c7fc31
Revises: f0e775390645
Create Date: 2021-03-25 10:17:15.049514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c9a9c7fc31'
down_revision = 'f0e775390645'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "investment_records",
        sa.Column("subscriber", sa.VARCHAR(50), nullable=False, index=True, server_default="")
    )
    op.add_column(
        "mutual_funds",
        sa.Column("subscriber", sa.VARCHAR(50), nullable=False, index=True, server_default="")
    )


def downgrade():
    op.drop_column(
        "investment_records",
        "subscriber"
    )
