"""Add inserted_at to workout

Revision ID: 3c61c6cefac6
Revises: bf85b1d6bd24
Create Date: 2024-09-28 16:16:14.592329

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3c61c6cefac6"
down_revision: Union[str, None] = "bf85b1d6bd24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workouts",
        sa.Column(
            "inserted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    op.drop_column("workouts", "inserted_at")
