from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ( Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters )
TOKEN = "8958924076:AAGmNgBxMsOIqQ_MZxYNfZQIuQv0dBpAg1M"
user_states = {} user_rtmp = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("محمد اللحيدان", callback_data="luhaidan")], [InlineKeyboardButton("ماهر المعيقلي", callback_data="muaiqly")], [InlineKeyboardButton("ياسر الدوسري", callback_data="dosary")] ]
await update.message.reply_text( "اختر القارئ:", reply_markup=InlineKeyboardMarkup(keyboard) ) 
async def addrtmp(update: Update, context: ContextTypes.DEFAULT_TYPE): user_states[update.effective_user.id] = "waiting_rtmp" await update.message.reply_text("ابعت رابط RTMP")
async def myrtmp(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id
if user_id not in user_rtmp: await update.message.reply_text("لا يوجد RTMP محفوظ") return await update.message.reply_text( f"RTMP الحالي:\n{user_rtmp[user_id]}" ) 
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id
if user_id not in user_states: return if user_states[user_id] == "waiting_rtmp": user_rtmp[user_id] = update.message.text del user_states[user_id] await update.message.reply_text( f"تم حفظ RTMP ✅\n\n{update.message.text}" ) 
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()
if query.from_user.id not in user_rtmp: await query.message.reply_text( "لا يوجد RTMP محفوظ\n\nاستخدم /addrtmp أولاً" ) return if query.data == "luhaidan": await query.message.reply_text( f"تم اختيار محمد اللحيدان\n\nسيتم البث على:\n{user_rtmp[query.from_user.id]}" ) elif query.data == "muaiqly": await query.message.reply_text( f"تم اختيار ماهر المعيقلي\n\nسيتم البث على:\n{user_rtmp[query.from_user.id]}" ) elif query.data == "dosary": await query.message.reply_text( f"تم اختيار ياسر الدوسري\n\nسيتم البث على:\n{user_rtmp[query.from_user.id]}" ) 
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("addrtmp", addrtmp)) app.add_handler(CommandHandler("myrtmp", myrtmp))
app.add_handler(CallbackQueryHandler(button_click)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.run_polling()
