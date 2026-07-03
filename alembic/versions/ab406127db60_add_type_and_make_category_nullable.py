"""add type and make category nullable

Revision ID: ab406127db60
Revises: 92540763ca40
Create Date: 2026-07-03 22:00:24.188624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab406127db60'
down_revision: Union[str, Sequence[str], None] = '92540763ca40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    columns = [row[1] for row in result]
    return column in columns


def upgrade() -> None:
    """Upgrade schema."""
    if not _column_exists("expenses", "type"):
        with op.batch_alter_table("expenses") as batch_op:
            batch_op.add_column(
                sa.Column("type", sa.String(), server_default="expense", nullable=False)
            )

    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "category", existing_type=sa.String(), nullable=True
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "category", existing_type=sa.String(), nullable=False
        )
        batch_op.drop_column("type")
