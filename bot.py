from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
ContextTypes,
MessageHandler,
filters
)
import sqlite3

TOKEN = "8958924076:AAGmNgBxMsOIqQ_MZxYNfZQIuQv0dBpAg1M"
OWNER_ID = 8128064754

user_states = {}

#Database

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS radios (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
url TEXT
)
""")

conn.commit()
conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT id,name FROM radios")
radios = cur.fetchall()

conn.close()

if not radios:
    await update.message.reply_text("لا توجد إذاعات مضافة")
    return

keyboard = []

for radio in radios:
    keyboard.append(
        [InlineKeyboardButton(radio[1], callback_data=f"radio_{radio[0]}")]
    )

await update.message.reply_text(
    "اختر الإذاعة:",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

async def addradio(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.effective_user.id != OWNER_ID:
await update.message.reply_text("غير مصرح")
return

user_states[update.effective_user.id] = "radio_name"
await update.message.reply_text("ابعت اسم الإذاعة")

async def listradios(update: Update, context: ContextTypes.DEFAULT_TYPE):
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT id,name FROM radios")
radios = cur.fetchall()

conn.close()

if not radios:
    await update.message.reply_text("لا توجد إذاعات")
    return

text = "الإذاعات:\n\n"

for radio in radios:
    text += f"{radio[0]} - {radio[1]}\n"

await update.message.reply_text(text)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id

if user_id not in user_states:
    return

state = user_states[user_id]

if state == "radio_name":
    context.user_data["radio_name"] = update.message.text
    user_states[user_id] = "radio_url"

    await update.message.reply_text("ابعت رابط الإذاعة")

elif state == "radio_url":

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO radios(name,url) VALUES(?,?)",
        (
            context.user_data["radio_name"],
            update.message.text
        )
    )

    conn.commit()
    conn.close()

    del user_states[user_id]

    await update.message.reply_text("تمت إضافة الإذاعة ✅")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

radio_id = query.data.replace("radio_", "")

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute(
    "SELECT name,url FROM radios WHERE id=?",
    (radio_id,)
)

radio = cur.fetchone()

conn.close()

if radio:
    await query.message.reply_text(
        f"📻 {radio[0]}\n\n{radio[1]}"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addradio", addradio))
app.add_handler(CommandHandler("listradios", listradios))

app.add_handler(
MessageHandler(
filters.TEXT & ~filters.COMMAND,
text_handler
)
)

app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()
