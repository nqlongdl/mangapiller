import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_USER_ID = int(os.getenv("DISCORD_USER_ID"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))

MANGA_URL = "https://mangapill.com/chapters"