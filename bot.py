import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '[8715899990:AAGI1lZPOgvG5XAGvHb4b7WsgjVn4iXuiFA]')
AUTHORIZED_USER_IDS = [5212493080]  # List of authorized Telegram User IDs

# --- Authorization Check ---
async def check_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        print(f"Unauthorized access attempt from user ID: {user_id}")
        return False
    return True

# --- Bot Commands and Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_authorization(update, context):
        return
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am your personal assistant bot. How can I help you today?",
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_authorization(update, context):
        return
    # Simple intelligent response based on message content
    text = update.message.text.lower()
    if "hello" in text or "hi" in text:
        response = "Hello there! How can I assist you?"
    elif "how are you" in text:
        response = "I'm a bot, so I don't have feelings, but I'm ready to help you!"
    elif "thank you" in text or "thanks" in text:
        response = "You're most welcome! Is there anything else?"
    elif "time" in text:
        import datetime
        response = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    else:
        response = "I received your message. How can I help you further?"
    
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")
    if update.effective_message:
        await update.effective_message.reply_text(
            "An error occurred while processing your request. Please try again later."
        )

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error_handler)

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
