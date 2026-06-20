from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8489184890:AAHLrgKqEL3wVwPwduQpV3V-_g5aQC5aPk8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("محمد اللحيدان", callback_data="luhaidan")],
        [InlineKeyboardButton("ماهر المعيقلي", callback_data="muaiqly")],
        [InlineKeyboardButton("ياسر الدوسري", callback_data="dosary")],
    ]

    await update.message.reply_text(
        "اختر القارئ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
