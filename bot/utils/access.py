from bot.config import ALLOWED_USER_IDS


async def check_access(update):

    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:

        await update.message.reply_text(
            "У вас нет доступа к этому боту."
        )

        return False

    return True