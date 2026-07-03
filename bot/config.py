import os

from dotenv import load_dotenv


load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Переменная окружения {name} не задана")

    return value


TOKEN = _require_env("BOT_TOKEN")

FID = int(_require_env("FIRST_ID"))

SID = int(_require_env("SECOND_ID"))

ALLOWED_USER_IDS = [FID, SID]

GOOGLE_SHEET_ID = _require_env("GOOGLE_SHEET_ID")

TIMEZONE = "Europe/Minsk"