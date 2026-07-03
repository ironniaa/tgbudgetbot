from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

from bot.utils.access import check_access

from bot.database.database import SessionLocal

from bot.models.expense import Expense

from bot.config import TIMEZONE


def _breakdown_lines(entries, owner_title, category_title):

    lines = []

    by_owner = defaultdict(float)

    by_category = defaultdict(float)

    for entry in entries:
        by_owner[entry.owner] += entry.amount
        by_category[entry.category] += entry.amount

    lines.append(owner_title)

    for owner, amount in sorted(by_owner.items(), key=lambda item: -item[1]):
        lines.append(f"  {owner}: {amount:.2f}")

    lines.append("")
    lines.append(category_title)

    for category, amount in sorted(by_category.items(), key=lambda item: -item[1]):
        lines.append(f"  {category}: {amount:.2f}")

    return lines


async def stats(update, context):

    if not await check_access(update):
        return

    now = datetime.now(ZoneInfo(TIMEZONE))

    month_start = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    db = SessionLocal()

    try:
        entries = (
            db.query(Expense)
            .filter(Expense.created_at >= month_start)
            .all()
        )
    finally:
        db.close()

    if not entries:

        await update.message.reply_text(
            "В этом месяце пока нет операций."
        )

        return

    expenses = [e for e in entries if e.type == "expense"]

    incomes = [e for e in entries if e.type == "income"]

    total_expense = sum(e.amount for e in expenses)

    total_income = sum(e.amount for e in incomes)

    balance = total_income - total_expense

    lines = [
        f"📊 Статистика за {month_start.strftime('%m.%Y')}",
        "",
        f"💰 Доходы: {total_income:.2f}",
        f"💸 Расходы: {total_expense:.2f}",
        f"📈 Остаток: {balance:.2f}",
    ]

    if expenses:
        lines.append("")
        lines.extend(
            _breakdown_lines(expenses, "Расходы по владельцам:", "Расходы по категориям:")
        )

    if incomes:
        lines.append("")
        lines.extend(
            _breakdown_lines(incomes, "Доходы по владельцам:", "Доходы по источникам:")
        )

    await update.message.reply_text("\n".join(lines))
