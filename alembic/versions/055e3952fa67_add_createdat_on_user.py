"""add createdAt on user

Revision ID: 055e3952fa67
Revises: 9992c90bb7a4
Create Date: 2024-07-10 15:37:45.590756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '055e3952fa67'
down_revision: Union[str, None] = '9992c90bb7a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
