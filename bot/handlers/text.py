from bot.utils.access import check_access

from bot.utils.keyboards import main_keyboard

from bot.utils.categories import CATEGORIES

from bot.utils.parser import normalize_category

from bot.database.database import SessionLocal

from bot.models.expense import Expense

from bot.services.sync_service import (
    sync_unsynced_expenses,
)


async def text_handler(update, context):

    if not await check_access(update):
        return

    text = update.message.text

    step = context.user_data.get("step")

    # =========================
    # COMMENT STEP
    # =========================

    if step == "comment":

        comment = text

        if comment == "-":
            comment = ""

        owner = context.user_data.get("owner")

        category = context.user_data.get("category")

        amount = context.user_data.get("amount")

        db = SessionLocal()

        expense = Expense(
            owner=owner,
            category=category,
            amount=amount,
            comment=comment,
        )

        db.add(expense)

        db.commit()

        db.close()

        sync_unsynced_expenses()

        context.user_data.clear()

        await update.message.reply_text(
            f"✅ {category}: {amount}",
            reply_markup=main_keyboard(),
        )

        return

    # =========================
    # AMOUNT STEP
    # =========================

    if step == "amount":

        try:
            amount = float(text)
        except:
            await update.message.reply_text(
                "Введите сумму числом"
            )
            return

        context.user_data["amount"] = amount

        context.user_data["step"] = "comment"

        await update.message.reply_text(
            "Комментарий?\n"
            "Или отправь -"
        )

        return

    # =========================
    # QUICK INPUT
    # =========================

    parts = text.lower().split()

    if len(parts) < 2:
        return

    raw_category = parts[0]

    category = normalize_category(raw_category)

    try:
        amount = float(parts[1])
    except:
        return

    extra_comment = (
        " ".join(parts[2:])
        if len(parts) > 2
        else ""
    )

    comment_parts = []

    if raw_category != category:
        comment_parts.append(raw_category)

    if extra_comment:
        comment_parts.append(extra_comment)

    comment = " | ".join(comment_parts)

    owner = update.effective_user.username

    db = SessionLocal()

    expense = Expense(
        owner=owner,
        category=category,
        amount=amount,
        comment=comment,
    )

    db.add(expense)

    db.commit()

    db.close()

    sync_unsynced_expenses()

    await update.message.reply_text(
        f"✅ {category}: {amount}",
        reply_markup=main_keyboard(),
    )