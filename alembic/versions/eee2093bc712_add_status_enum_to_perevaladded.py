from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'eee2093bc712'
down_revision: Union[str, None] = '65e716910f76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        ALTER TABLE pereval_added
        ADD CONSTRAINT check_status
        CHECK (status IN ('new', 'pending', 'accepted', 'rejected'))
    """)

def downgrade() -> None:
    op.execute("""
        ALTER TABLE pereval_added
        DROP CONSTRAINT check_status
    """)
