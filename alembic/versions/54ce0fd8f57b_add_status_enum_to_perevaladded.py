"""Add status enum to PerevalAdded

Revision ID: 54ce0fd8f57b
Revises: eee2093bc712
Create Date: 2024-11-14 04:12:57.522610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54ce0fd8f57b'
down_revision: Union[str, None] = 'eee2093bc712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
