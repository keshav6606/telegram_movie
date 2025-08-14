import os
import logging
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------- CONFIG ----------
API_ID = int(os.getenv("API_ID", 26954495))
API_HASH = os.getenv("API_HASH", "2061c55207cfee4f106ff0dc331fe3d9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8347005060:AAHf11nTICnku70OKIcX8OccXr8DlhKa17s")

BACKEND_URL = os.getenv("BACKEND_URL", "https://tiny-theadora-filetolink7-6059208b.koyeb.app")
SITE_URL = os.getenv("SITE_URL", "http://filmy4uhd.vercel.app")

# ---------- LOGGING ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- BOT INIT ----------
app = Client(
    "movie_search_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------- START COMMAND ----------
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply_text(
        "**🎬 Welcome to Movie Bot!**\n\n"
        "Just send me the name of a movie or series, and I'll give you the watch link."
    )

# ---------- MOVIE SEARCH ----------
@app.on_message(filters.text & filters.private)
async def movie_search(client, message: Message):
    query = message.text.strip()
    if not query:
        return await message.reply_text("❌ Please send a valid movie name.")

    try:
        # Backend search API
        resp = requests.get(f"{BACKEND_URL}/search", params={"q": query})
        if resp.status_code != 200:
            return await message.reply_text("⚠️ Error fetching data from backend.")

        results = resp.json()
        if not results:
            return await message.reply_text("❌ No results found.")

        # Send first result
        movie = results[0]
        title = movie.get("title") or movie.get("name") or "Untitled"
        movie_id = movie.get("id")

        await message.reply_text(
            f"**{title}**\n\n"
            f"[🎥 Watch Here]({SITE_URL}/movie/{movie_id})",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(e)
        await message.reply_text("⚠️ Something went wrong. Please try again later.")

# ---------- RUN ----------
if __name__ == "__main__":
    app.run()
