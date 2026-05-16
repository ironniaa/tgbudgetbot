from bot.utils.access import check_access

from bot.utils.keyboards import (
    categories_keyboard,
)


async def mode_handler(update, context):

    if not await check_access(update):
        return

    text = update.message.text

    username = update.effective_user.username

    if text == "Личное":

        context.user_data["owner"] = username

    elif text == "Общее":

        context.user_data["owner"] = "общее"

    else:
        return

    context.user_data["step"] = "category"

    await update.message.reply_text(
        "Выбери категорию:",
        reply_markup=categories_keyboard(),
    )