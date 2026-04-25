import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

main_menu = ReplyKeyboardMarkup([
    ["📦 پکیج های ایلای", "⬜ ارزیابی رایگان"],
    ["🧳 مشاوره ایلای", "📋 تهیه مدارک ایلای"],
    ["✈️ پکیج های ویزا", "📞 ارتباط با پشتیبانی"]
], resize_keyboard=True)

packages_menu = ReplyKeyboardMarkup([
    ["🇪🇺 پکیج های اروپا", "🇨🇦🇺🇸 پکیج آمریکای شمالی"],
    ["🇨🇦 پکیج کانادا", "🇦🇺🇳🇿 پکیج استرالیا و نیوزیلند"],
    ["📝 پکیج مکاتبه با اساتید", "🎓 پکیج کارشناسی"],
    ["🎓 پکیج پست داک", "🧑‍🏫 پکیج منتورینگ"],
    ["↩️ بازگشت"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 سلام {name}\n\n"
        "🌟 به ربات رسمی مجموعه ایلای فور فری خوش اومدی!\n\n"
        "👇 از منوی زیر سرویس مورد نظر رو انتخاب کن",
        reply_markup=main_menu
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 پکیج های ایلای":
        await update.message.reply_text("لطفا پکیج مورد نظر رو انتخاب کنید:", reply_markup=packages_menu)
    elif text == "↩️ بازگشت":
        await update.message.reply_text("منوی اصلی:", reply_markup=main_menu)
    elif text == "📞 ارتباط با پشتیبانی":
        await update.message.reply_text("برای پشتیبانی به @your_id پیام بدید.")
    elif text == "⬜ ارزیابی رایگان":
        await update.message.reply_text("لینک ارزیابی رایگان: your-link.com")
    elif text == "🧑‍🏫 پکیج منتورینگ":
        await update.message.reply_text("توضیحات پکیج منتورینگ اینجا...")
    else:
        await update.message.reply_text("لطفا از منو انتخاب کن 👇", reply_markup=main_menu)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
