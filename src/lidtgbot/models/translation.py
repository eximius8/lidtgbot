from dataclasses import dataclass
from typing import Literal


@dataclass
class Translation:
    language_code: Literal['de', 'en', 'tr', 'ru', 'fr', 'ar', 'uk', 'hi']
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    context: str
