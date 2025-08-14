from pyrogram import Client, filters
import requests

# ====== CONFIG ======
BOT_TOKEN = "8347005060:AAHf11nTICnku70OKIcX8OccXr8DlhKa17s"
API_ID = 26954495
API_HASH = "2061c55207cfee4f106ff0dc331fe3d9"
BACKEND_URL = "https://tiny-theadora-filetolink7-6059208b.koyeb.app"
SITE_URL = "http://filmy4uhd.vercel.app"

# ====== BOT INIT ======
app = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("movie") & filters.private)
def movie_search(client, message):
    query = " ".join(message.command[1:]).strip()
    if not query:
        message.reply_text("❗ Please provide a movie name.\nExample: `/movie Weapons`", quote=True)
        return

    try:
        # Step 1: Call backend search API
        search_url = f"{BACKEND_URL}/search?query={query}"
        res = requests.get(search_url)
        res.raise_for_status()
        data = res.json()

        if not data or "results" not in data or not data["results"]:
            message.reply_text("⚠ No results found for your query.")
            return

        # Step 2: Take the first result
        first_item = data["results"][0]
        movie_id = first_item.get("id")
        content_type = first_item.get("type")  # Expected: "movie", "series", "tvshow"

        if not movie_id or not content_type:
            message.reply_text("⚠ API response is missing 'id' or 'type'.")
            return

        # Step 3: Build final URL
        final_url = f"{SITE_URL}/{content_type}/{movie_id}"

        # Step 4: Send response
        message.reply_text(
            f"🎬 **Title:** {first_item.get('title', 'Unknown')}\n"
            f"🔗 **Link:** {final_url}"
        )

    except Exception as e:
        message.reply_text(f"❌ Error: {e}")

# ====== START BOT ======
print("Bot is running...")
app.run()
