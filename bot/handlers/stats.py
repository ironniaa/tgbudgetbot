from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense

from bot.config import TIMEZONE


async def stats(update, context):

    if not await check_access(update):
        return

    now = datetime.now(ZoneInfo(TIMEZONE))

    month_start = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    db = SessionLocal()

    try:
        expenses = (
            db.query(Expense)
            .filter(Expense.created_at >= month_start)
            .all()
        )
    finally:
        db.close()

    if not expenses:

        await update.message.reply_text(
            "В этом месяце пока нет трат."
        )

        return

    total = sum(expense.amount for expense in expenses)

    by_owner = defaultdict(float)

    by_category = defaultdict(float)

    for expense in expenses:
        by_owner[expense.owner] += expense.amount
        by_category[expense.category] += expense.amount

    lines = [
        f"📊 Статистика за {month_start.strftime('%m.%Y')}",
        "",
        f"Всего: {total:.2f}",
        "",
        "По владельцам:",
    ]

    for owner, amount in sorted(by_owner.items(), key=lambda item: -item[1]):
        lines.append(f"  {owner}: {amount:.2f}")

    lines.append("")
    lines.append("По категориям:")

    for category, amount in sorted(by_category.items(), key=lambda item: -item[1]):
        lines.append(f"  {category}: {amount:.2f}")

    await update.message.reply_text("\n".join(lines))
