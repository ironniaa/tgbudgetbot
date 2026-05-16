import os

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

FID = int(os.getenv("FIRST_ID"))

SID = int(os.getenv("SECOND_ID"))

ALLOWED_USER_IDS = [FID, SID]