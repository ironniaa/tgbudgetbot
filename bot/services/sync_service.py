from bot.database.database import SessionLocal
from bot.models.expense import Expense

from bot.services.google_sheets import append_expenses


def sync_unsynced_expenses():

    db = SessionLocal()

    unsynced = (
        db.query(Expense)
        .filter(Expense.synced == False)
        .all()
    )

    if not unsynced:
        db.close()
        return

    append_expenses(unsynced)

    for expense in unsynced:
        expense.synced = True

    db.commit()

    db.close()