from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(os.getenv("LOCAL_DATA_DIR", "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
NOTES_FILE = DATA_DIR / "notes.jsonl"


def append_note(note: Dict[str, Any]) -> Dict[str, Any]:
    note = dict(note)
    note.setdefault("id", f"note_{int(datetime.now(tz=timezone.utc).timestamp()*1000)}")
    note.setdefault("created_at", datetime.now(tz=timezone.utc).isoformat())
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(note, ensure_ascii=False) + "\n")
    return note


def load_notes() -> List[Dict[str, Any]]:
    if not NOTES_FILE.exists():
        return []
    with NOTES_FILE.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
