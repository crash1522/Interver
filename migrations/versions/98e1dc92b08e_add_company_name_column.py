"""Add company_name column

Revision ID: 98e1dc92b08e
Revises: a5c6a6baa8fd
Create Date: 2024-04-17 20:49:01.435072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98e1dc92b08e'
down_revision: Union[str, None] = 'a5c6a6baa8fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('record', sa.Column('company_name', sa.String(), nullable=True))

def downgrade():
    op.drop_column('record', 'company_name')
