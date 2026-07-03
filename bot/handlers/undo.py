import logging

from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense

from bot.services.google_sheets import rewrite_sheet


logger = logging.getLogger(__name__)


async def undo(update, context):

    if not await check_access(update):
        return

    username = update.effective_user.username

    db = SessionLocal()

    try:
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

            return

        category = expense.category

        amount = expense.amount

        db.delete(expense)

        db.commit()

    finally:
        db.close()

    sheet_note = ""

    try:
        rewrite_sheet()
    except Exception:
        logger.exception("Не удалось обновить Google Sheet после /undo")
        sheet_note = "\n⚠️ Не удалось обновить таблицу, попробуйте позже"

    await update.message.reply_text(
        f"Удалено:\n"
        f"{category} — {amount}{sheet_note}"
    )
