from bot.utils.categories import CATEGORIES


def normalize_category(word: str):

    word = word.lower()

    for category, aliases in CATEGORIES.items():

        if word in aliases:
            return category

    return word