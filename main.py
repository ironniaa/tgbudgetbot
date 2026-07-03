import asyncio
import logging
from logging.handlers import RotatingFileHandler

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import TOKEN

from bot.database.init_db import init_db

from bot.handlers.start import start

from bot.handlers.reset import reset

from bot.handlers.mode import mode_handler

from bot.handlers.text import text_handler

from bot.handlers.history import history

from bot.handlers.undo import undo

from bot.handlers.stats import stats

from bot.handlers.callbacks import callbacks

from bot.services.backup_service import run_backup

from telegram.ext import CallbackQueryHandler

init_db()

# Alembic (внутри init_db) переконфигурирует root-логгер через fileConfig(),
# поэтому наши handlers ставятся только после миграций и с force=True.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            "bot.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        ),
    ],
    force=True,
)

logger = logging.getLogger(__name__)

BACKUP_INTERVAL_SECONDS = 24 * 60 * 60


async def _periodic_backup_loop():
    while True:
        try:
            await asyncio.to_thread(run_backup)
        except Exception:
            logger.exception("Плановый бэкап не удался")

        await asyncio.sleep(BACKUP_INTERVAL_SECONDS)


async def _post_init(application):
    asyncio.create_task(_periodic_backup_loop())


app = ApplicationBuilder().token(TOKEN).post_init(_post_init).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("reset", reset)
)

app.add_handler(
    MessageHandler(
        filters.Regex("^(Личное|Общее)$"),
        mode_handler,
    )
)

app.add_handler(
    CallbackQueryHandler(callbacks)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_handler,
    )
)

app.add_handler(
    CommandHandler("history", history)
)

app.add_handler(
    CommandHandler("undo", undo)
)

app.add_handler(
    CommandHandler("stats", stats)
)


async def error_handler(update, context):

    logger.error(
        "Необработанная ошибка при обработке обновления",
        exc_info=context.error,
    )

    message = (
        update.effective_message
        if isinstance(update, Update)
        else None
    )

    if message is not None:
        try:
            await message.reply_text(
                "Что-то пошло не так, попробуйте позже."
            )
        except Exception:
            logger.exception("Не удалось уведомить пользователя об ошибке")


app.add_error_handler(error_handler)

logger.info("Bot started")

app.run_polling()
