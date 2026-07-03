import csv
import logging
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from bot.config import TIMEZONE
from bot.services.google_sheets import get_worksheet_values


logger = logging.getLogger(__name__)

BACKUP_DIR = Path("backups")

DATABASE_PATH = Path("database.db")

RETENTION = 14

SHEETS_TO_EXPORT = ["operations", "dashboard"]


def _timestamp():
    return datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y%m%d_%H%M%S")


def _prune_old_backups(pattern):
    files = sorted(BACKUP_DIR.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    for old_file in files[RETENTION:]:
        old_file.unlink(missing_ok=True)


def backup_database():

    if not DATABASE_PATH.exists():
        return

    BACKUP_DIR.mkdir(exist_ok=True)

    dest = BACKUP_DIR / f"database_{_timestamp()}.db"

    shutil.copy2(DATABASE_PATH, dest)

    _prune_old_backups("database_*.db")

    logger.info("Database backup written to %s", dest)


def backup_sheets():

    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = _timestamp()

    for sheet_name in SHEETS_TO_EXPORT:

        values = get_worksheet_values(sheet_name)

        dest = BACKUP_DIR / f"{sheet_name}_{timestamp}.csv"

        with open(dest, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(values)

        _prune_old_backups(f"{sheet_name}_*.csv")

        logger.info("Sheet '%s' backup written to %s", sheet_name, dest)


def run_backup():
    backup_database()

    try:
        backup_sheets()
    except Exception:
        logger.exception("Failed to back up Google Sheets")
