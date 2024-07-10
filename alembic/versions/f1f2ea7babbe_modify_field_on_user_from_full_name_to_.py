"""modify field on user from full_name to name

Revision ID: f1f2ea7babbe
Revises: 2d7addd67fa5
Create Date: 2024-07-10 14:25:17.927163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1f2ea7babbe'
down_revision: Union[str, None] = '2d7addd67fa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
