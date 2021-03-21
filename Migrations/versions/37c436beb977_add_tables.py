"""add tables

Revision ID: 37c436beb977
Revises: 
Create Date: 2021-03-21 09:20:27.763611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37c436beb977'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mutual_funds",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('identifier', sa.VARCHAR(20), nullable=False, index=True),
        sa.Column('name', sa.VARCHAR(255), nullable=False, index=True),
        sa.Column('is_deleted', sa.BOOLEAN, nullable=False, index=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False,
                  server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    )
    op.create_unique_constraint(
        constraint_name='uq_mutual_funds',
        table_name='mutual_funds',
        columns=['identifier', 'name', 'is_deleted']
    )

    op.create_table(
        "investment_records",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('fund_identifier', sa.VARCHAR(20), nullable=False, index=True),
        sa.Column('nav', sa.FLOAT, nullable=False, index=True),
        sa.Column('units', sa.FLOAT, nullable=False, index=True),
        sa.Column('execution_date', sa.TIMESTAMP, nullable=False, index=True),
        sa.Column('is_deleted', sa.BOOLEAN, nullable=False, index=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False,
                  server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    )


def downgrade():
    op.drop_table("mutual_funds")
    op.drop_table("investment_records")
