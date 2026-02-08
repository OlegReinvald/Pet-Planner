from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import dateparser
from dateparser.search import search_dates
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


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


def _default_due(note_type: str) -> Optional[datetime]:
    tz = ZoneInfo("Europe/Minsk")
    now = datetime.now(tz=tz)

    if note_type == "task":
        return (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    if note_type == "buy":
        return now.replace(hour=19, minute=0, second=0, microsecond=0)
    return None


def parse_note(text: str) -> ParsedNote:
    note_type = classify(text)
    cleaned = strip_command(text)
    settings = {
        "PREFER_DATES_FROM": "future",
        "RETURN_AS_TIMEZONE_AWARE": True,
        "TIMEZONE": "Europe/Minsk",
    }

    dt = dateparser.parse(cleaned, languages=["ru", "en"], settings=settings)
    if not dt:
        found = search_dates(cleaned, languages=["ru", "en"], settings=settings)
        if found:
            dt = found[0][1]
    if not dt:
        dt = _default_due(note_type)
    due = dt.isoformat() if dt else None
    return ParsedNote(title=cleaned.strip(), note_type=note_type, due=due)
