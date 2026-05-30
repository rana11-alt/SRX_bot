import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটআপ (বোটের কার্যক্রম ট্র্যাক করার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# আপনার বোট টোকেন
TOKEN = "7738804330:AAEYizHtBCaUdoo5O5bPhtpJ4yTXIV_c3TA"

# আপনার টেলিগ্রাম গ্রুপের লিংক (এখানে আপনার আসল গ্রুপ লিংকটি বসিয়ে দিন)
GROUP_LINK = "https://t.me/green2life2024" 

# /start কমান্ড দিলে যে মেসেজ এবং বাটন শো করবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Join Our Group 🚀", url=GROUP_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        user_name = update.message.from_user.first_name
text = "🎉🤩 Welcome, {user_name}! 🌟🎁 Exclusive offers 💰 and incredible giveaways are live right now! 🚀💥 Don't miss out on this gold rush! 🏃💨 Click the button below and join our group immediately! 👇✨"
,
        reply_markup=reply_markup
    )

# কেউ মেসেজ দিলে যে অটো-রিপ্লাই যাবে
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.lower()
    
    # বাটন সেটআপ
    keyboard = [[InlineKeyboardButton("Join Our Group 🚀", url=GROUP_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ইউজার 'hi' বা 'hello' লিখলে এই রিপ্লাই যাবে
    if "hi" in user_text or "hello" in user_text:
        await update.message.reply_text(
            text="হ্যালো! আশা করি ভালো আছেন। আমাদের গ্রুপে যুক্ত হতে নিচের বাটনে ক্লিক করুন:",
            reply_markup=reply_markup
        )
    # অন্য কিছু লিখলে এই ডিফল্ট রিপ্লাই যাবে (এটি আপনি আপনার মতো পরিবর্তন করতে পারবেন)
    else:
        await update.message.reply_text(
            text="ধন্যবাদ আপনার মেসেজের জন্য! আমাদের অফিশিয়াল গ্রুপে যোগ দিতে নিচের বাটনটি ব্যবহার করুন:",
            reply_markup=reply_markup
        )

def main() -> None:
    # বোট অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(TOKEN).build()

    # হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    # বোট রান করা
    print("বোটটি সফলভাবে চালু হয়েছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
