import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# আপনার সঠিক বোট টোকেনটি এখানে বসাবেন
TOKEN = "7738804330:AAEYizHtBCaUdoo5O5bPhtpJ4yTXIV_c3TA"

# সচল গ্রুপ আইডিগুলো জমা রাখার জন্য একটি সেট (Set)
# এর ফলে বটটি যতগুলো গ্রুপে অ্যাড হবে, সবগুলোর আইডি এখানে স্বয়ংক্রিয়ভাবে জমা হবে
ACTIVE_GROUPS = set()

# ৩০ সেকেন্ড পর পর এই ফাংশনটি সব গ্রুপে মেসেজ পাঠাবে
async def send_spam_message(context: ContextTypes.DEFAULT_TYPE):
    if not ACTIVE_GROUPS:
        return # কোনো গ্রুপে অ্যাড না থাকলে কিছুই করবে না

    text = (
        "🎉🤩 **Welcome Everyone!** 🌟🎁\n\n"
        "Exclusive offers 💰 and incredible giveaways are live right now! 🚀💥\n"
        "Don't miss out on this gold rush! 🏃💨\n\n"
        "Click the button below and join our group immediately! 👇✨"
    )
    
    # তালিকায় থাকা প্রতিটি গ্রুপে লুপ চালিয়ে মেসেজ পাঠানো হবে
    for chat_id in list(ACTIVE_GROUPS):
        try:
            await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"গ্রুপ {chat_id}-এ মেসেজ পাঠানো যায়নি (হয়তো বটকে রিমুভ করা হয়েছে): {e}")
            # যদি বটকে গ্রুপ থেকে বের করে দেওয়া হয় বা মেসেজ ব্লক করা হয়, তবে তালিকা থেকে বাদ যাবে
            ACTIVE_GROUPS.discard(chat_id)

# বট নতুন কোনো গ্রুপে অ্যাড হলে বা গ্রুপ থেকে রিমুভ হলে এই ফাংশনটি কাজ করবে
async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    chat_id = result.chat.id
    new_status = result.new_chat_member.status

    # বট গ্রুপে অ্যাড হলে (মেম্বার বা অ্যাডমিন হিসেবে)
    if new_status in ["member", "administrator"]:
        ACTIVE_GROUPS.add(chat_id)
        logging.info(f"নতুন গ্রুপে যুক্ত হয়েছি! আইডি: {chat_id}")
        # গ্রুপে ঢোকার সাথে সাথে প্রথম একটা স্বাগত মেসেজ দিবে
        try:
            await context.bot.send_message(chat_id=chat_id, text="🤖 বটটি সফলভাবে গ্রুপে সক্রিয় হয়েছে এবং অফার মেসেজ পাঠানো শুরু করছে!")
        except Exception as e:
            pass
            
    # বটকে গ্রুপ থেকে বের করে দিলে বা লেফট নিলে
    elif new_status in ["left", "kicked"]:
        ACTIVE_GROUPS.discard(chat_id)
        logging.info(f"গ্রুপ থেকে রিমুভ করা হয়েছে। আইডি: {chat_id}")

def main():
    # অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(TOKEN).build()

    # বট কোন কোন গ্রুপে আছে তা ট্র্যাক করার হ্যান্ডলার
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    # JobQueue সেটআপ করা (৩০ সেকেন্ড পর পর রান হবে)
    job_queue = application.job_queue
    job_queue.run_repeating(send_spam_message, interval=30, first=10)

    # বট চালু করা
    print("ডাইনামিক বটটি সফলভাবে চালু হয়েছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
