from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers.start import start_conversation_handler, menu
from handlers.menu import handle_menu


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # /start registration flow
    app.add_handler(start_conversation_handler)

    # /menu command
    app.add_handler(CommandHandler("menu", menu))

    # menu button text handling
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()