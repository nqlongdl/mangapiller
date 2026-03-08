import asyncio
import io
import requests
import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil import parser
import discord
from discord.ext import commands
from threading import Thread
import uvicorn

import config
import db
from logger import logger
from api import app, set_bot

SCRAPE_HEADERS = {
    "Referer": "https://mangapill.com/",
}

# --- Alert owner on error ---
async def alert_error(client, message: str):
    try:
        user = await client.fetch_user(config.DISCORD_USER_ID)
        await user.send(f"⚠️ **Mangapiller Error**\n```{message}```")
    except Exception as e:
        logger.error("Failed to send error alert: %s", e)

# --- Scrape ---
def scrape():
    logger.info("Start scraping %s", config.MANGA_URL)
    try:
        r = requests.get(config.MANGA_URL, timeout=20)
        logger.info("HTTP status: %s", r.status_code)
        r.raise_for_status()
    except Exception as e:
        logger.error("HTTP request failed: %s", e)
        raise

    soup = BeautifulSoup(r.text, "html.parser")
    all_blocks = soup.select("div")
    logger.debug("Total divs found: %d", len(all_blocks))

    seen = set()
    results = []
    favorites = [f.lower() for f in db.get_favorites()]
    for block in all_blocks:
        title_tag = block.select_one(".text-sm.font-bold")
        if not title_tag:
            continue

        title_lower = title_tag.text.lower()
        if not any(x in title_lower for x in favorites):
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

        # Display title: capitalize + chapter number
        display_title = title_tag.text.strip()
        chapter_tag = block.select_one(".mt-3.text-lg.font-black")
        chapter_num = chapter_tag.text.strip() if chapter_tag else ""

        img_tag = block.select_one("img[data-src]")
        thumbnail = img_tag["data-src"] if img_tag else None

        results.append({
            "title": f"{display_title} {chapter_num}".strip(),
            "url": url,
            "thumbnail": thumbnail
        })

    logger.info("Favorite chapters found today: %d", len(results))
    for r in results:
        logger.info(" -> %s | %s", r['title'], r['url'])

    return results

# --- Fetch thumbnail ---
async def fetch_image(url: str) -> bytes | None:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=10, follow_redirects=True, headers=SCRAPE_HEADERS)
            if r.status_code == 200:
                return r.content
            logger.warning("Thumbnail fetch returned %s for %s", r.status_code, url)
    except Exception as e:
        logger.error("Failed to fetch thumbnail: %s", e)
    return None

# --- Notify ---
async def notify(client, items):
    try:
        user = await client.fetch_user(config.DISCORD_USER_ID)
    except Exception as e:
        logger.error("Failed to fetch Discord user: %s", e)
        await alert_error(client, f"Failed to fetch Discord user: {e}")
        return

    logger.info("Sending %d notifications...", len(items))
    for item in items:
        if db.already_sent(item["url"]):
            logger.info("Already sent: %s", item['title'])
            continue

        embed = discord.Embed(
            title=item["title"],
            url=item["url"],
            color=discord.Color.orange()
        )

        file = None
        if item["thumbnail"]:
            img_bytes = await fetch_image(item["thumbnail"])
            if img_bytes:
                file = discord.File(io.BytesIO(img_bytes), filename="thumbnail.jpg")
                embed.set_image(url="attachment://thumbnail.jpg")

        try:
            await user.send(content=f"🔔 **{item['title']}** just dropped!", file=file, embed=embed)
            logger.info("Sent: %s", item["title"])
            db.mark_sent(item["url"])
        except Exception as e:
            logger.error("Failed to send for %s: %s", item["title"], e)
            await alert_error(client, f"Failed to send notification for '{item['title']}': {e}\n{item['url']}")

# --- Worker ---
async def worker(client):
    await client.wait_until_ready()
    logger.info("Bot ready, entering worker loop...")

    while True:
        try:
            db.cleanup_sent()            
            logger.info("Checking for updates...")
            items = await asyncio.to_thread(scrape)
            if items:
                await notify(client, items)
            else:
                logger.info("No new chapters today.")
        except Exception as e:
            logger.error("Worker error: %s", e)
            await alert_error(client, f"Worker error during scrape: {e}")

        logger.info("Sleeping for %d seconds...\n", config.CHECK_INTERVAL)
        await asyncio.sleep(config.CHECK_INTERVAL)

# --- Discord bot ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="check", description="Check for new manga chapters now")
async def check_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        items = await asyncio.to_thread(scrape)
        new_items = [item for item in items if not db.already_sent(item["url"])]
        if new_items:        
            await notify(bot, items)
            await interaction.followup.send(f"✅ Found {len(items)} new chapter(s)!", ephemeral=True)
        else:
            await interaction.followup.send("😴 No new chapters today.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)
        await alert_error(bot, f"/check command error: {e}")

async def do_check():
    items = await asyncio.to_thread(scrape)
    new_items = [item for item in items if not db.already_sent(item["url"])]
    if new_items:
        await notify(bot, items)
    return len(new_items)

@bot.event
async def on_ready():
    set_bot(bot)
    await bot.tree.sync()
    logger.info("Discord bot connected! Slash commands synced.")
    bot.loop.create_task(worker(bot))

# --- Run FastAPI in thread ---
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# --- Main ---
if __name__ == "__main__":
    Thread(target=run_api, daemon=True).start()
    bot.run(config.DISCORD_TOKEN)