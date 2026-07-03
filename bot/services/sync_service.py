import logging

from bot.database.database import SessionLocal
from bot.models.expense import Expense

from bot.services.google_sheets import append_expenses


logger = logging.getLogger(__name__)


def sync_unsynced_expenses():
    """Возвращает True, если все несинхронизированные траты успешно ушли в Google Sheets."""

    db = SessionLocal()

    try:
        unsynced = (
            db.query(Expense)
            .filter(Expense.synced == False)
            .all()
        )

        if not unsynced:
            return True

        append_expenses(unsynced)

        for expense in unsynced:
            expense.synced = True

        db.commit()

        return True

    except Exception:
        logger.exception("Не удалось синхронизировать траты с Google Sheets")
        db.rollback()
        return False

    finally:
        db.close()