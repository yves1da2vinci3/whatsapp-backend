"""add nullable on other field

Revision ID: 9992c90bb7a4
Revises: f1f2ea7babbe
Create Date: 2024-07-10 14:36:28.972382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9992c90bb7a4'
down_revision: Union[str, None] = 'f1f2ea7babbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
