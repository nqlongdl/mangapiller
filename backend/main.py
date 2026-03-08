import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil import parser
import discord
from threading import Thread
import uvicorn

import config
import db
from logger import logger
from api import app  # FastAPI app

# --- Scrape ---
def scrape():
    logger.info("Start scraping %s", config.MANGA_URL)
    try:
        r = requests.get(config.MANGA_URL, timeout=20)
        logger.info("HTTP status: %s", r.status_code)
    except Exception as e:
        logger.error("HTTP request failed: %s", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    all_blocks = soup.select("div")
    logger.debug("Total divs found: %d", len(all_blocks))

    seen = set()
    results = []
    favorites = db.get_favorites()
    for block in all_blocks:
        title_tag = block.select_one(".text-sm.font-bold")
        if not title_tag:
            continue

        title = title_tag.text.lower()
        if not any(x in title for x in favorites):
            continue

        link_tag = block.select_one("a[href^='/chapters']")
        if not link_tag:
            continue

        url = "https://mangapill.com" + link_tag["href"]
        if url in seen:
            continue
        seen.add(url)        

        time_tag = block.select_one("time-ago")
        if not time_tag:
            continue

        dt = parser.isoparse(time_tag["datetime"])
        now = datetime.now(timezone.utc)
        if dt.date() != now.date():
            continue

        results.append({"title": title, "url": url})

    logger.info("Favorite chapters found today: %d", len(results))
    for r in results:
        logger.info(" -> %s | %s", r['title'], r['url'])

    return results

# --- Notify ---
async def notify(client, items):
    try:
        user = await client.fetch_user(config.DISCORD_USER_ID)
    except Exception as e:
        logger.error("Failed to fetch Discord user: %s", e)
        return

    logger.info("Sending %d notifications...", len(items))
    for item in items:
        if db.already_sent(item["url"]):
            logger.info("Already sent: %s", item['title'])
            continue

        msg = f"New chapter\n{item['title']}\n{item['url']}"
        try:
            await user.send(msg)
            logger.info("Sent: %s", item['title'])
            db.mark_sent(item["url"])
        except Exception as e:
            logger.error("Failed to send Discord message for %s: %s", item['title'], e)

# --- Worker ---
async def worker(client):
    await client.wait_until_ready()
    logger.info("Bot ready, entering worker loop...")

    while True:
        try:
            logger.info("Checking for updates...")
            items = scrape()
            if items:
                await notify(client, items)
            else:
                logger.info("No new chapters today.")
        except Exception as e:
            logger.error("Worker error: %s", e)

        logger.info("Sleeping for %d seconds...\n", config.CHECK_INTERVAL)
        await asyncio.sleep(config.CHECK_INTERVAL)

# --- Discord client ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info("Discord bot connected!")

# --- Run FastAPI in thread ---
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# --- Main ---
if __name__ == "__main__":
    # Start FastAPI in separate thread
    Thread(target=run_api, daemon=True).start()

    # Run bot + worker in asyncio loop
    async def main():
        asyncio.create_task(worker(client))
        await client.start(config.DISCORD_TOKEN)

    asyncio.run(main())