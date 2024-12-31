"""add content column to posts table

Revision ID: c795b3f92db4
Revises: 8536d8363706
Create Date: 2024-12-30 17:24:14.211431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c795b3f92db4'
down_revision: Union[str, None] = '8536d8363706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False))   
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
