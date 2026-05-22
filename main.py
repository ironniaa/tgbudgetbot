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

from bot.handlers.callbacks import callbacks

from telegram.ext import CallbackQueryHandler

init_db()

app = ApplicationBuilder().token(TOKEN).build()


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

print("Bot started")

app.run_polling()