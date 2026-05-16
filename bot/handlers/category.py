from bot.utils.access import check_access

from bot.utils.categories import CATEGORY_MAP


async def category_handler(update, context):

    if not await check_access(update):
        return

    if context.user_data.get("step") != "category":
        return

    text = update.message.text

    if text not in CATEGORY_MAP:
        return

    context.user_data["category"] = CATEGORY_MAP[text]

    context.user_data["step"] = "amount"

    await update.message.reply_text(
        "Введи сумму:"
    )