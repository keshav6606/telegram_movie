import os
import httpx
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Config
API_ID = int(os.getenv("API_ID", "26954495"))
API_HASH = os.getenv("API_HASH", "2061c55207cfee4f106ff0dc331fe3d9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8347005060:AAHf11nTICnku70OKIcX8OccXr8DlhKa17s")
BACKEND_URL = os.getenv("BACKEND_URL", "https://tiny-theadora-filetolink7-6059208b.koyeb.app")
SITE_URL = os.getenv("SITE_URL", "http://filmy4uhd.vercel.app")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "8"))

app = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text.strip()
    if not query:
        await message.reply_text("Please type a movie name to search.")
        return

    search_url = f"{BACKEND_URL}/search?query={query}&page=1&size={PAGE_SIZE}"
    try:
        async with httpx.AsyncClient() as client_http:
            r = await client_http.get(search_url)
            if r.status_code != 200:
                await message.reply_text("Error fetching movies from backend.")
                return
            movies = r.json()
    except Exception as e:
        await message.reply_text(f"Error: {e}")
        return

    if not movies:
        await message.reply_text("No movies found.")
        return

    for movie in movies:
        title = movie.get("title") or movie.get("name")
        poster = movie.get("poster")
        tmdb_id = movie.get("tmdb_id")
        watch_link = f"{SITE_URL}/watch/{tmdb_id}"

        buttons = [[InlineKeyboardButton("🎬 Watch Now", url=watch_link)]]
        try:
            if poster:
                await message.reply_photo(
                    poster,
                    caption=f"**{title}**",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await message.reply_text(
                    f"**{title}**
{watch_link}",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
        except Exception:
            await message.reply_text(
                f"**{title}**
{watch_link}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

if __name__ == "__main__":
    app.run()
