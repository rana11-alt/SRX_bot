import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Your Bot Token
TOKEN = "7738804330:AAEYizHtBCaUdoo5O5bPhtpJ4yTXIV_c3TA"

# Set to store active group IDs automatically
ACTIVE_GROUPS = set()

# Function to send messages to all active groups every 30 seconds
async def send_spam_message(context: ContextTypes.DEFAULT_TYPE):
    if not ACTIVE_GROUPS:
        return # Do nothing if not added to any group

    text = (
        "🎉🤩 **Welcome Everyone!** 🌟🎁\n\n"
        "Exclusive offers 💰 and incredible giveaways are live right now! 🚀💥\n"
        "Don't miss out on this gold rush! 🏃💨\n\n"
        "Click the button below and join our group immediately! 👇✨"
        
    )
    
    # Inline Button Setup
    keyboard = [
        [
            InlineKeyboardButton("Join Channel 🚀", url="https://t.me/green2life2024")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Loop through all saved groups and send the message with the button
    for chat_id in list(ACTIVE_GROUPS):
        try:
            await context.bot.send_message(
                chat_id=chat_id, 
                text=text, 
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        except Exception as e:
            logging.error(f"Could not send message to group {chat_id} (Bot might be removed): {e}")
            # Remove group ID if the bot is blocked or kicked
            ACTIVE_GROUPS.discard(chat_id)

# Handler to track when the bot is added or removed from groups
async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    chat_id = result.chat.id
    new_status = result.new_chat_member.status

    # If bot is added as member or administrator
    if new_status in ["member", "administrator"]:
        ACTIVE_GROUPS.add(chat_id)
        logging.info(f"Added to a new group! ID: {chat_id}")
        
        # Send a welcome message immediately upon joining
        try:
            await context.bot.send_message(chat_id=chat_id, text="🤖 Bot has been successfully activated in this group!")
        except Exception as e:
            pass
            
    # If bot is removed or left the group
    elif new_status in ["left", "kicked"]:
        ACTIVE_GROUPS.discard(chat_id)
        logging.info(f"Removed from group. ID: {chat_id}")

def main():
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Handler to track chat members status
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    # JobQueue setup (runs every 30 seconds, starts after 10 seconds)
    job_queue = application.job_queue
    job_queue.run_repeating(send_spam_message, interval=30, first=10)

    # Start the bot
    print("Dynamic bot started successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
