import json
import os
import requests

from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
MessageHandler,
ContextTypes,
filters,
)

# =========================

# ENV VARIABLES

# =========================

TOKEN = os.getenv("TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DB_FILE = "aquarium_db.json"

# =========================

# DATABASE

# =========================

def load_db():
with open(DB_FILE, "r", encoding="utf-8") as f:
return json.load(f)

def search_item(text, db):
text = text.lower()

```
for category in db:
    for item in db[category]:

        fa = item.get("fa_name", "").lower()
        en = item.get("en_name", "").lower()

        if fa and fa in text:
            return item

        if en and en in text:
            return item

return None
```

# =========================

# OPENROUTER

# =========================

def ask_gemma(question):

```
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "google/gemma-4-31b-it:free",
        "messages": [
            {
                "role": "system",
                "content": """
```

You are a professional aquarium expert.

Rules:

* Answer in Persian if the user speaks Persian.
* Answer in English if the user speaks English.
* Focus on aquarium topics.
* Fish
* Aquatic plants
* Amphibians
* Shrimp
* Snails
* Terrariums
* Aquascaping
* Water chemistry

If the question is unrelated to aquariums,
politely answer that you specialize in aquarium topics.
"""
},
{
"role": "user",
"content": question
}
],
"temperature": 0.7
},
timeout=60
)

```
response.raise_for_status()

data = response.json()

return data["choices"][0]["message"]["content"]
```

# =========================

# COMMANDS

# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
await update.message.reply_text(
    "🌿 Aquarium Bot Online\n\n"
    "نام ماهی، گیاه یا سوال آکواریومی خود را ارسال کنید."
)
```

# =========================

# MESSAGE HANDLER

# =========================

async def handle_message(
update: Update,
context: ContextTypes.DEFAULT_TYPE
):

```
text = update.message.text

if not text:
    return

db = load_db()

# فقط در صورت تگ شدن در گروه پاسخ بده
if update.message.chat.type in ["group", "supergroup"]:

    bot_username = context.bot.username.lower()

    if bot_username not in text.lower():
        return

item = search_item(text, db)

# =====================
# DATABASE ANSWER
# =====================

if item:

    reply = f"""
```

🐠 {item.get('fa_name', '')} / {item.get('en_name', '')}

🇮🇷 {item.get('fa_desc', '')}
🇬🇧 {item.get('en_desc', '')}

🌡 Temp: {item.get('temp', '')}
⚗️ pH: {item.get('ph', '')}

🧼 Care

🇮🇷 {item.get('care', {}).get('fa', '')}
🇬🇧 {item.get('care', {}).get('en', '')}
"""

```
    await update.message.reply_text(reply)

    return

# =====================
# GEMMA ANSWER
# =====================

try:

    await update.message.chat.send_action("typing")

    answer = ask_gemma(text)

    if len(answer) > 4000:
        answer = answer[:4000]

    await update.message.reply_text(answer)

except Exception as e:

    print("OPENROUTER ERROR:", e)

    await update.message.reply_text(
        "❌ خطا در ارتباط با هوش مصنوعی"
    )
```

# =========================

# MAIN

# =========================

def main():

```
if not TOKEN:
    print("❌ TOKEN not found")
    return

if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY not found")
    return

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("🤖 Aquarium Bot Running...")

app.run_polling()
```

if **name** == "**main**":
main()
