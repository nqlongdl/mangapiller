import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_USER_ID = int(os.getenv("DISCORD_USER_ID"))

CHECK_INTERVAL = 86400

MANGA_URL = "https://mangapill.com/chapters"