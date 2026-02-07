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

COMMAND_MAP = {
    "/task": "task",
    "/idea": "idea",
    "/buy": "buy",
    "/note": "note",
}


def classify(text: str) -> str:
    lower = text.lower()
    for cmd, t in COMMAND_MAP.items():
        if lower.startswith(cmd):
            return t
    for t, words in KEYWORDS.items():
        if any(w in lower for w in words):
            return t
    return "note"


def strip_command(text: str) -> str:
    lower = text.lower()
    for cmd in COMMAND_MAP:
        if lower.startswith(cmd):
            return text[len(cmd):].strip() or text
    return text


def parse_note(text: str) -> ParsedNote:
    note_type = classify(text)
    cleaned = strip_command(text)
    dt = dateparser.parse(
        cleaned,
        languages=["ru", "en"],
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": True,
            "TIMEZONE": "Europe/Warsaw",
        },
    )
    due = dt.isoformat() if dt else None
    return ParsedNote(title=cleaned.strip(), note_type=note_type, due=due)
