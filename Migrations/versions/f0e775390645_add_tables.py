"""add tables

Revision ID: f0e775390645
Revises: 37c436beb977
Create Date: 2021-03-21 19:52:36.171784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0e775390645'
down_revision = '37c436beb977'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "nav_histories",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('fund_identifier', sa.VARCHAR(20), nullable=False, index=True),
        sa.Column('fund_name', sa.VARCHAR(255), nullable=False, index=True),
        sa.Column('nav', sa.FLOAT, nullable=False, index=True),
        sa.Column('date', sa.TIMESTAMP, nullable=False, index=True),
        sa.Column('is_deleted', sa.BOOLEAN, nullable=False, index=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False,
                  server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    )


def downgrade():
    op.drop_table("nav_histories")
