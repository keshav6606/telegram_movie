import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import urllib.parse

# ---------------- CONFIG ----------------
BOT_TOKEN = "8347005060:AAHf11nTICnku70OKIcX8OccXr8DlhKa17s"
BACKEND_API_BASE = "https://tiny-theadora-filetolink7-6059208b.koyeb.app"
SITE_URL = "http://filmy4uhd.vercel.app"

# --------------- HANDLER -----------------
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("⚠ Please type a movie/TV show name.")
        return

    try:
        # 1️⃣ Search in backend
        search_url = f"{BACKEND_API_BASE}/api/search/?query={urllib.parse.quote(query)}&page=1&page_size=1"
        search_res = requests.get(search_url, timeout=10).json()

        if not search_res.get("results"):
            await update.message.reply_text("❌ No results found.")
            return

        first_result = search_res["results"][0]
        tmdb_id = first_result.get("tmdb_id")
        title = first_result.get("title", "Unknown Title")

        # 2️⃣ Get movie details
        detail_url = f"{BACKEND_API_BASE}/api/id/{tmdb_id}"
        details = requests.get(detail_url, timeout=10).json()
        files = details.get("files")

        if not files:
            await update.message.reply_text("⚠ No downloadable files found for this title.")
            return

        # Pick the first file
        file_info = files[0]
        encoded_id = file_info["encoded_id"]
        file_name = file_info["file_name"]

        # 3️⃣ Prepare links
        watch_link = f"{SITE_URL}/watch/{tmdb_id}"
        download_link = f"{BACKEND_API_BASE}/dl/{encoded_id}/{urllib.parse.quote(file_name)}"

        # 4️⃣ Send result
        reply_text = (
            f"🎬 <b>{title}</b>\n"
            f"🆔 <b>TMDB ID:</b> <code>{tmdb_id}</code>\n"
            f"▶ <a href=\"{watch_link}\">Watch Online</a>\n"
            f"⬇ <a href=\"{download_link}\">Download / Stream</a>"
        )
        await update.message.reply_html(reply_text, disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {str(e)}")


# ---------------- MAIN -------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    print("🤖 Bot is running...")
    app.run_polling()


        first_result = search_res["results"][0]
        tmdb_id = first_result.get("tmdb_id")
        title = first_result.get("title", "Unknown Title")

        # Get file details
        detail_url = f"{BACKEND_API_BASE}/api/id/{tmdb_id}"
        details = requests.get(detail_url, timeout=10).json()
        files = details.get("files")
        if not files:
            await update.message.reply_text("No downloadable files found for this title.")
            return

        file_info = files[0]  # Take the first file, can be adapted for quality selection
        encoded_id = file_info["encoded_id"]
        file_name = file_info["file_name"]

        watch_link = f"{SITE_URL}/watch/{tmdb_id}"
        download_link = f"{BACKEND_API_BASE}/dl/{encoded_id}/{urllib.parse.quote(file_name)}"

        reply_text = (
            f"🎬 <b>{title}</b>\n"
            f"🆔 <b>TMDB ID:</b> <code>{tmdb_id}</code>\n"
            f"▶ <a href=\"{watch_link}\">Watch Online</a>\n"
            f"⬇ <a href=\"{download_link}\">Download/Stream</a>"
        )
        await update.message.reply_html(reply_text, disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    print("🤖 Bot is running…")
    app.run_polling()
