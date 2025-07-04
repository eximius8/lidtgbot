import logging
from telegram import Update, User
from telegram.ext import ContextTypes
from lidtgbot.database.user import user_repository
from lidtgbot.handlers.decorators import require_user

logger = logging.getLogger(__name__)

@require_user
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User) -> None:
    """Handle /start command"""
    try:
        # Create or get user from database
        db_user = await user_repository.get_or_create_user(
            user_id=user.id,
            first_name=user.first_name,
            username=user.username,
            last_name=user.last_name,
            language_code=user.language_code
        )
        
        logger.info(f"User {user.id} ({user.first_name}) started the bot")
        
        await update.message.reply_text(
            f"Hallo {user.first_name}! Willkommen beim Leben in Deutschland Test Bot! 🇩🇪\n\n"
            "Ich kann dir dabei helfen, dich auf den Test vorzubereiten."
        )
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "Entschuldigung, ein Fehler ist aufgetreten. Versuche es später noch einmal."
        )