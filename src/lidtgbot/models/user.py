from dataclasses import dataclass
from datetime import datetime
from lidtgbot.models.federal_state import FederalState


@dataclass
class User:
    user_id: int
    first_name: str
    created_at: datetime
    updated_at: datetime
    total_questions_answered: int = 0
    username: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    federal_state: FederalState | None = None
