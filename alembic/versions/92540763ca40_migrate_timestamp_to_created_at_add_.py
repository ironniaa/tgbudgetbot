"""migrate timestamp to created_at add timezone

Revision ID: 92540763ca40
Revises: 2e627a97fe6a
Create Date: 2026-05-22 21:35:15.132501

"""
from typing import Sequence, Union
from datetime import datetime
from zoneinfo import ZoneInfo

from alembic import op
import sqlalchemy as sa


revision: str = '92540763ca40'
down_revision: Union[str, Sequence[str], None] = '2e627a97fe6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TIMEZONE = "Europe/Minsk"


def _column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    columns = [row[1] for row in result]
    return column in columns


def upgrade() -> None:
    if not _column_exists("expenses", "timestamp"):
        return

    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column("timestamp", new_column_name="created_at")

    if not _column_exists("expenses", "timezone"):
        with op.batch_alter_table("expenses") as batch_op:
            batch_op.add_column(
                sa.Column("timezone", sa.String(), server_default=TIMEZONE, nullable=False)
            )

    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT id, created_at FROM expenses")).fetchall()
    tz = ZoneInfo(TIMEZONE)
    for row_id, ts_str in rows:
        if ts_str:
            utc_dt = datetime.fromisoformat(ts_str).replace(tzinfo=ZoneInfo("UTC"))
            local_dt = utc_dt.astimezone(tz)
            bind.execute(
                sa.text("UPDATE expenses SET created_at = :dt WHERE id = :id"),
                {"dt": local_dt.isoformat(), "id": row_id},
            )


def downgrade() -> None:
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column("created_at", new_column_name="timestamp")
        batch_op.drop_column("timezone")
