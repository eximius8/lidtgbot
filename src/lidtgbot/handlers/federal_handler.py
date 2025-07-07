import logging
from telegram import Update, User
from telegram.ext import ContextTypes
from lidtgbot.handlers.decorators import require_user_with_db
from lidtgbot.models.user import User as DbUser
from lidtgbot.keyboards.federal import create_federal_keyboard

logger = logging.getLogger(__name__)


@require_user_with_db
async def federal_command(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                       telegram_user: User, db_user: DbUser) -> None:
    """Handle /start command"""
    logger.info(f"User {telegram_user.id} ({telegram_user.first_name}) invoked federal command")
    
    await update.message.reply_text(
        f"Hallo {telegram_user.first_name}! Willkommen beim Leben in Deutschland Test Bot! 🇩🇪\n\n"
        "Ich kann dir dabei helfen, dich auf den Test vorzubereiten.",
        reply_markup=create_federal_keyboard(db_user)
    )

