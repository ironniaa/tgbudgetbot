from bot.utils.inline_keyboards import (
    categories_inline,
)


async def callbacks(update, context):

    query = update.callback_query

    await query.answer()

    data = query.data

    # =====================
    # PAGE SWITCH
    # =====================

    if data.startswith("page:"):

        page = int(
            data.split(":")[1]
        )

        await query.edit_message_reply_markup(
            reply_markup=categories_inline(page)
        )

        return

    # =====================
    # CATEGORY
    # =====================

    if data.startswith("cat:"):

        category = data.split(":")[1]

        context.user_data["category"] = category

        context.user_data["step"] = "amount"

        await query.message.reply_text(
            f"Категория: {category}\n\n"
            "Введи сумму:"
        )

        return