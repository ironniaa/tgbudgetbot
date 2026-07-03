import logging

from bot.config import ALLOWED_USER_IDS


logger = logging.getLogger(__name__)


async def check_access(update):

    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:

        logger.info("Отказан доступ пользователю user_id=%s", user_id)

        await update.message.reply_text(
            "У вас нет доступа к этому боту."
        )

        return False

    return True