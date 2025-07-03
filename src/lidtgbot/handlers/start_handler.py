from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    await update.message.reply_text("Hallo! Willkommen beim Leben in Deutschland Test Bot! 🇩🇪")