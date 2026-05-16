from telegram import ReplyKeyboardMarkup


def main_keyboard():

    return ReplyKeyboardMarkup(
        [
            ["Личное", "Общее"],
        ],
        resize_keyboard=True,
    )


def categories_keyboard():

    keyboard = [
        ["🍔 Еда", "🚕 Транспорт"],
        ["🏠 Квартира", "🧴 Хоз"],
        ["🎮 Развлечения"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )