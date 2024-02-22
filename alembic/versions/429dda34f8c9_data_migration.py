"""Data Migration

Revision ID: 429dda34f8c9
Revises: 3e0024f6568e
Create Date: 2024-02-21 16:52:56.882705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '429dda34f8c9'
down_revision: Union[str, None] = '3e0024f6568e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT INTO role (role) VALUES ('admin'), ('buyer'), ('seller')"
    )

