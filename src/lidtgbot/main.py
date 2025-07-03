import os
import logging
from telegram.ext import Application, CommandHandler
from lidtgbot.handlers.start_handler import start_command

logging.basicConfig(level=logging.INFO)

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.run_polling()

if __name__ == "__main__":
    main()