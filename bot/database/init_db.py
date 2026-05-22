import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

from bot.database.database import engine
from bot.models.expense import Base
from bot.config import TIMEZONE


def _get_column_names(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def _migrate_schema():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    tables = [
        r[0] for r in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    ]

    if "expenses" not in tables:
        conn.close()
        return

    columns = _get_column_names(cursor, "expenses")

    if "timestamp" in columns and "created_at" not in columns:
        cursor.execute(
            "ALTER TABLE expenses RENAME COLUMN timestamp TO created_at"
        )
        cursor.execute("SELECT id, created_at FROM expenses")
        rows = cursor.fetchall()
        tz = ZoneInfo(TIMEZONE)
        for row_id, ts_str in rows:
            if ts_str:
                utc_dt = datetime.fromisoformat(ts_str).replace(
                    tzinfo=ZoneInfo("UTC")
                )
                local_dt = utc_dt.astimezone(tz)
                cursor.execute(
                    "UPDATE expenses SET created_at = ? WHERE id = ?",
                    (local_dt.isoformat(), row_id),
                )
        conn.commit()

    columns = _get_column_names(cursor, "expenses")
    if "timezone" not in columns:
        cursor.execute(
            f"ALTER TABLE expenses ADD COLUMN timezone TEXT DEFAULT '{TIMEZONE}'"
        )
        cursor.execute(
            f"UPDATE expenses SET timezone = '{TIMEZONE}' WHERE timezone IS NULL"
        )
        conn.commit()

    conn.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_schema()