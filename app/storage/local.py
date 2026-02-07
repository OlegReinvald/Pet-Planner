from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

def _data_dir() -> Path:
    data_dir = Path(os.getenv("LOCAL_DATA_DIR", "./data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def _notes_file() -> Path:
    return _data_dir() / "notes.jsonl"


def append_note(note: Dict[str, Any]) -> Dict[str, Any]:
    note = dict(note)
    note.setdefault("id", f"note_{int(datetime.now(tz=timezone.utc).timestamp()*1000)}")
    note.setdefault("created_at", datetime.now(tz=timezone.utc).isoformat())
    notes_file = _notes_file()
    with notes_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(note, ensure_ascii=False) + "\n")
    return note


def load_notes() -> List[Dict[str, Any]]:
    notes_file = _notes_file()
    if not notes_file.exists():
        return []
    with notes_file.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
