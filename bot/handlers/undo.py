from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense

from bot.services.google_sheets import rewrite_sheet

async def undo(update, context):

    if not await check_access(update):
        return

    username = update.effective_user.username

    db = SessionLocal()

    expense = (
        db.query(Expense)
        .filter(Expense.creator == username)
        .order_by(Expense.id.desc())
        .first()
    )

    if not expense:

        await update.message.reply_text(
            "Нечего удалять"
        )

        db.close()

        return

    category = expense.category

    amount = expense.amount

    db.delete(expense)

    db.commit()

    rewrite_sheet()

    db.close()

    await update.message.reply_text(
        f"Удалено:\n"
        f"{category} — {amount}"
    )