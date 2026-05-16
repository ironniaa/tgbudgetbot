from bot.utils.access import check_access

from bot.utils.keyboards import main_keyboard


async def start(update, context):

    if not await check_access(update):
        return

    context.user_data.clear()

    await update.message.reply_text(
        "Выбери режим:",
        reply_markup=main_keyboard(),
    )