import logging
from functools import wraps
from telegram import Update, User
from telegram.ext import ContextTypes
from typing import Callable, Awaitable
from lidtgbot.database.user import user_repository
from lidtgbot.models.user import User as DbUser

logger = logging.getLogger(__name__)


def require_user(func: Callable[[Update, ContextTypes.DEFAULT_TYPE, User], Awaitable[None]]):
    """
    Base decorator that ensures update.effective_user exists and is not a bot.
    Passes the validated user as a third parameter to the handler.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        # Check if user exists
        if user is None:
            logger.warning("Received update with no effective_user")
            return
        
        # Ignore bots
        if user.is_bot:
            logger.info(f"Bot {user.id} ({user.first_name}) ignored in {func.__name__}")
            return
        
        # Call the original function with the validated user
        return await func(update, context, user)
    
    return wrapper


def ensure_user_in_db(update_activity: bool = False):
    """
    Decorator factory that ensures user is in database.
    Must be used with @require_user decorator.
    
    Args:
        update_activity: Whether to update user activity timestamp
    """
    def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE, User, DbUser], Awaitable[None]]):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
            try:
                # Ensure user exists in database with single call
                db_user = await user_repository.ensure_user(
                    user_id=user.id,
                    first_name=user.first_name,
                    username=user.username,
                    last_name=user.last_name,
                    language_code=user.language_code,
                    update_activity=update_activity
                )
                
                # Call the original function with both user objects
                return await func(update, context, user, db_user)
                
            except Exception as e:
                logger.error(f"Database error for user {user.id}: {e}")
                if update.message:
                    await update.message.reply_text(
                        "Entschuldigung, ein Fehler ist aufgetreten. Versuche es später noch einmal."
                    )
                return
        
        return wrapper
    return decorator


# Convenience decorators for common use cases
def require_user_with_db(func: Callable[[Update, ContextTypes.DEFAULT_TYPE, User, DbUser], Awaitable[None]]):
    """
    Convenience decorator that combines @require_user and @ensure_user_in_db()
    without activity update.
    """
    return require_user(ensure_user_in_db(update_activity=False)(func))


def require_user_with_db_activity(func: Callable[[Update, ContextTypes.DEFAULT_TYPE, User, DbUser], Awaitable[None]]):
    """
    Convenience decorator that combines @require_user and @ensure_user_in_db(update_activity=True)
    """
    return require_user(ensure_user_in_db(update_activity=True)(func))