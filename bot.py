from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8958924076:AAGmNgBxMsOIqQ_MZxYNfZQIuQv0dBpAg1M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("محمد اللحيدان", callback_data="luhaidan")],
        [InlineKeyboardButton("ماهر المعيقلي", callback_data="muaiqly")],
        [InlineKeyboardButton("ياسر الدوسري", callback_data="dosary")]
    ]

    await update.message.reply_text(
        "اختر القارئ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "luhaidan":
        await query.message.reply_text("تم اختيار محمد اللحيدان")

    elif query.data == "muaiqly":
        await query.message.reply_text("تم اختيار ماهر المعيقلي")

    elif query.data == "dosary":
        await query.message.reply_text("تم اختيار ياسر الدوسري")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()
