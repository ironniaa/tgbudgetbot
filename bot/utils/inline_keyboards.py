from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


CATEGORIES_PAGES = [
    [
        ("🍔 Еда", "еда"),
        ("🚕 Транспорт", "транспорт"),
        ("🏠 Квартира", "квартира"),
    ],

    [
        ("🧴 Хоз", "хоз"),
        ("🎮 Развлечения", "развлечения"),
        ("💊 Здоровье", "здоровье"),
        ("💅 Уход", "уход"),
    ],
]


def categories_inline(page=0):

    categories = CATEGORIES_PAGES[page]

    keyboard = []

    for text, value in categories:

        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"cat:{value}",
            )
        ])

    navigation = []

    if page > 0:

        navigation.append(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"page:{page - 1}",
            )
        )

    if page < len(CATEGORIES_PAGES) - 1:

        navigation.append(
            InlineKeyboardButton(
                "➡️",
                callback_data=f"page:{page + 1}",
            )
        )

    if navigation:
        keyboard.append(navigation)

    return InlineKeyboardMarkup(keyboard)