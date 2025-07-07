import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lidtgbot.models.user import User
from lidtgbot.models.federal_state import FEDERAL_STATES

logger = logging.getLogger(__name__)


def create_federal_keyboard(db_user: User) -> InlineKeyboardMarkup:
    federal_states_list = list(FEDERAL_STATES.values())
    keyboard = []
    for i in range(0, len(federal_states_list), 2):
        row = []
        for j in range(2):
            if i + j < len(federal_states_list):
                state = federal_states_list[i + j]
                button_text = f"{state.emoji} {state.name_de}"
                # Add checkmark if this is the current state
                if db_user.federal_state == state.code:
                    button_text = f"✅ {button_text}"
                
                row.append(InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"federal_{state.code}"
                ))
        keyboard.append(row)
    
    # Add cancel button
    keyboard.append([InlineKeyboardButton("❌ Abbrechen", callback_data="federal_cancel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
