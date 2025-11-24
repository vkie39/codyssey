"""create question table

Revision ID: 1ef9baeabc47
Revises: 
Create Date: 2025-11-24 19:22:57.836951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ef9baeabc47'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 예시 답변에대한 테이블을 추가 시 출력
def upgrade() -> None:
    """Upgrade schema."""
    pass

#삭제 기능
def downgrade() -> None:
    """Downgrade schema."""
    pass
