from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense


async def history(update, context):

    if not await check_access(update):
        return

    username = update.effective_user.username

    db = SessionLocal()

    expenses = (
        db.query(Expense)
        .order_by(Expense.id.desc())
        .limit(10)
        .all()
    )

    db.close()

    if not expenses:

        await update.message.reply_text(
            "История пуста"
        )

        return

    message = "Последние операции:\n\n"

    for expense in expenses:

            message += (
        f"• [{expense.owner}] "
        f"{expense.category} — "
        f"{expense.amount}\n"
        f"внес: {expense.creator}\n\n"
    )

    await update.message.reply_text(message)