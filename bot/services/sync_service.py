from bot.database.database import SessionLocal
from bot.models.expense import Expense

from bot.services.google_sheets import operations_sheet


def sync_unsynced_expenses():

    db = SessionLocal()

    unsynced = (
        db.query(Expense)
        .filter(Expense.synced == False)
        .all()
    )

    for expense in unsynced:

        operations_sheet.append_row([
            expense.id,
            str(expense.timestamp),
            expense.creator,
            expense.owner,
            expense.category,
            expense.amount,
            expense.comment,
        ])

        expense.synced = True

    db.commit()

    db.close()