from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class Question:
    num: str
    solution: Literal['a', 'b', 'c', 'd']
    category: str
    created_at: datetime
    updated_at: datetime
    image: str | None = None
