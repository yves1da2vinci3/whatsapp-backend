"""add createdTime in message

Revision ID: bde767047125
Revises: 055e3952fa67
Create Date: 2024-07-10 23:07:41.732463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bde767047125'
down_revision: Union[str, None] = '055e3952fa67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
