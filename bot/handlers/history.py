from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense


async def history(update, context):

    if not await check_access(update):
        return

    username = update.effective_user.username

    filter_arg = context.args[0].lower() if context.args else None

    db = SessionLocal()

    try:
        query = db.query(Expense).order_by(Expense.created_at.desc())

        if filter_arg == "личное":
            query = query.filter(Expense.owner == username)
        elif filter_arg == "общее":
            query = query.filter(Expense.owner == "общее")

        expenses = query.limit(10).all()

    finally:
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

        is_income = expense.type == "income"

        icon = "💰" if is_income else "💸"

        sign = "+" if is_income else "-"

        message += (
            f"• {icon} [{expense.owner}] "
            f"{expense.category} — "
            f"{sign}{expense.amount}\n"
            f"{date_str} | внес: {expense.creator}\n\n"
        )

    await update.message.reply_text(message)
