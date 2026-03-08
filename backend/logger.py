import logging
import os

LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "manga.log")

# setup logger
logger = logging.getLogger("manga_notifier")
logger.setLevel(logging.INFO)

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(ch_formatter)

# file handler
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.INFO)
fh.setFormatter(ch_formatter)

logger.addHandler(ch)
logger.addHandler(fh)