from bot.utils.keyboards import main_keyboard


async def reset(update, context):

    context.user_data.clear()

    await update.message.reply_text(
        "Состояние сброшено.",
        reply_markup=main_keyboard(),
    )