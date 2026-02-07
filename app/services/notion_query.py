from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def _headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def query_due_notes(now: Optional[datetime] = None) -> List[Dict]:
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return []
    now = now or datetime.now(tz=timezone.utc)
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "Дата окончания", "date": {"on_or_before": now.isoformat()}},
                {"property": "Статус", "select": {"does_not_equal": "Выполнено"}},
            ]
        }
    }
    r = requests.post(url, headers=_headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


def extract_chat_id(page: Dict) -> Optional[str]:
    prop = page.get("properties", {}).get("ChatId", {})
    rich = prop.get("rich_text", [])
    if not rich:
        return None
    return rich[0].get("plain_text")


def mark_done(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": {"Статус": {"select": {"name": "Выполнено"}}}}
    r = requests.patch(url, headers=_headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
