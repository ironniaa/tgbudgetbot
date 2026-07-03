from bot.utils.categories import CATEGORIES

from bot.utils.income_sources import INCOME_SOURCES


def parse_amount(text: str) -> float:
    return float(text.replace(",", "."))


def resolve_transaction(word: str):

    word = word.lower()

    for category, aliases in CATEGORIES.items():

        if word in aliases:
            return "expense", category

    for source, aliases in INCOME_SOURCES.items():

        if word in aliases:
            return "income", source

    return "expense", word
