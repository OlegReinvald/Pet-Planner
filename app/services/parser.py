from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import dateparser


@dataclass
class ParsedNote:
    title: str
    note_type: str  # task/idea/buy/note
    due: Optional[str]  # ISO string


KEYWORDS = {
    "buy": ["купить", "покупки", "buy"],
    "idea": ["идея", "idea"],
    "task": ["сделать", "задача", "task"],
}


def classify(text: str) -> str:
    lower = text.lower()
    for t, words in KEYWORDS.items():
        if any(w in lower for w in words):
            return t
    return "note"


def parse_note(text: str) -> ParsedNote:
    note_type = classify(text)
    dt = dateparser.parse(text, languages=["ru", "en"])
    due = dt.isoformat() if dt else None
    return ParsedNote(title=text.strip(), note_type=note_type, due=due)
