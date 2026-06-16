import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 گرفتن توکن از Render Environment Variables
TOKEN = os.getenv("8434421974:AAGWJ-JUvdGeLU4e7TpHcqLQiKLj7BSpmvo")

DB_FILE = "aquarium_db.json"


# ---------- load database ----------
def load_db():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- search function ----------
def search_item(text, db):
    text = text.lower()

    for category in db:
        for item in db[category]:
            fa = item.get("fa_name", "").lower()
            en = item.get("en_name", "").lower()

            if fa and fa in text:
                return item
            if en and en in text:
                return item

    return None


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Aquarium Bot is online!\nSend fish or plant name."
    )


# ---------- message handler ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    db = load_db()

    # اگر گروه است، فقط وقتی تگ شده جواب بده
    if update.message.chat.type in ["group", "supergroup"]:
        bot_username = context.bot.username.lower()
        if bot_username not in text.lower():
            return

    item = search_item(text, db)

    if item:
        reply = f"""
🐠 {item.get('fa_name','')} / {item.get('en_name','')}

🇮🇷 {item.get('fa_desc','')}
🇬🇧 {item.get('en_desc','')}

🌡 Temp: {item.get('temp','')}
⚗️ pH: {item.get('ph','')}

🧼 Care:
🇮🇷 {item['care']['fa']}
🇬🇧 {item['care']['en']}
"""
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("❌ No information found / اطلاعاتی پیدا نشد")


# ---------- main ----------
def main():
    if not TOKEN:
        print("❌ TOKEN not found in environment variables!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
