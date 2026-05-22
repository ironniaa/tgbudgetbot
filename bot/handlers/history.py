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
        .order_by(Expense.created_at.desc())
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
        date_str = ""
        if expense.created_at:
            date_str = expense.created_at.strftime("%d.%m.%Y %H:%M")

        message += (
            f"• [{expense.owner}] "
            f"{expense.category} — "
            f"{expense.amount}\n"
            f"{date_str} | внес: {expense.creator}\n\n"
        )

    await update.message.reply_text(message)