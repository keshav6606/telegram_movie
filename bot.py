import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "8347005060:AAHf11nTICnku70OKIcX8OccXr8dlhKa17s")
BACKEND_URL = os.getenv("BACKEND_URL", "https://tiny-theadora-filetolink7-6059208b.koyeb.app")
SITE_URL = os.getenv("SITE_URL", "http://filmy4uhd.vercel.app")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Send me a movie name and I'll give you its link!")

# Search movie function
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("⚠ Please enter a movie name.")
        return

    try:
        response = requests.get(f"{BACKEND_URL}/search", params={"query": query}, timeout=10)
        data = response.json()

        if not data or "results" not in data or len(data["results"]) == 0:
            await update.message.reply_text("❌ No movie found.")
            return

        movie = data["results"][0]  # First search result
        title = movie.get("title", "Unknown Title")
        movie_id = movie.get("id", "")

        await update.message.reply_text(
            f"**{title}**\n\n"
            f"[🎥 Watch Here]({SITE_URL}/movie/{movie_id})",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠ An error occurred while searching for the movie.")

# Main function to run bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    logger.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
