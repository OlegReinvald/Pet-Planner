from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Dict, List

from app.storage.local import load_notes
from app.services.telegram import send_message


def due_notes(now: datetime | None = None) -> List[Dict]:
    now = now or datetime.now(tz=timezone.utc)
    out = []
    for note in load_notes():
        due = note.get("due")
        if not due or note.get("status") != "open":
            continue
        try:
            due_dt = datetime.fromisoformat(due)
        except Exception:
            continue
        if due_dt <= now:
            out.append(note)
    return out


def send_due_reminders():
    for note in due_notes():
        chat_id = note.get("chat_id")
        title = note.get("title")
        if chat_id and title:
            try:
                send_message(chat_id, f"Напоминание: {title}")
            except Exception:
                # ignore if no token in local mode
                pass
