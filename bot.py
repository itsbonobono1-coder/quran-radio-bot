from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8489184890:AAHLrgKqEL3wVwPwduQpV3V-_g5aQC5aPk8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت شغال ✅")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
