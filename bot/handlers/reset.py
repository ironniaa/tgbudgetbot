from bot.utils.access import check_access

from bot.utils.keyboards import main_keyboard


async def reset(update, context):

    if not await check_access(update):
        return

    context.user_data.clear()

    await update.message.reply_text(
        "Состояние сброшено.",
        reply_markup=main_keyboard(),
    )