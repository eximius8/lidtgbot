from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class Question:
    num: int
    solution: Literal['a', 'b', 'c', 'd']
    created_at: datetime
    updated_at: datetime
    image: str | None = None
