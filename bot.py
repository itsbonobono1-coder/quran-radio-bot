from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = "8489184890:AAHLrgKqEL3wVwPwduQpV3V-_g5aQC5aPk8"

user_states = {}

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

async def addrtmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_states[update.effective_user.id] = "waiting_name"
    await update.message.reply_text("ابعت اسم القناة")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state == "waiting_name":
        context.user_data["channel_name"] = update.message.text
        user_states[user_id] = "waiting_rtmp"
        await update.message.reply_text("ابعت RTMP")

    elif state == "waiting_rtmp":
        del user_states[user_id]
        await update.message.reply_text("تم حفظ القناة ✅")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addrtmp", addrtmp))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()
