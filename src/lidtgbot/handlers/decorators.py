import logging
from functools import wraps
from telegram import Update, User
from telegram.ext import ContextTypes
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)


def require_user(func: Callable[[Update, ContextTypes.DEFAULT_TYPE, User], Awaitable[None]]):
    """
    Decorator that ensures update.effective_user exists and is not a bot.
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