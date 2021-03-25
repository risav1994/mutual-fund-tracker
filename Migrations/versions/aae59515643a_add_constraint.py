"""add constraint

Revision ID: aae59515643a
Revises: 92c9a9c7fc31
Create Date: 2021-03-25 11:18:25.877964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aae59515643a'
down_revision = '92c9a9c7fc31'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        constraint_name='uq_mutual_funds',
        table_name='mutual_funds',
        type_='unique'
    )
    op.create_unique_constraint(
        constraint_name='uq_mutual_funds',
        table_name='mutual_funds',
        columns=['identifier', 'name', 'subscriber', 'is_deleted']
    )


def downgrade():
    op.drop_constraint(
        constraint_name='uq_mutual_funds',
        table_name='mutual_funds',
        type_='unique'
    )
    op.create_unique_constraint(
        constraint_name='uq_mutual_funds',
        table_name='mutual_funds',
        columns=['identifier', 'name', 'is_deleted']
    )
