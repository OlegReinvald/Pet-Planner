import os
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def create_note(title: str, note_type: str, due_iso: str | None, chat_id: str):
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        raise RuntimeError("NOTION_TOKEN/NOTION_DATABASE_ID not set")

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    properties = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Type": {"select": {"name": note_type}},
        "Source": {"rich_text": [{"text": {"content": "Telegram"}}]},
        "ChatId": {"rich_text": [{"text": {"content": str(chat_id)}}]},
        "Status": {"select": {"name": "open"}},
    }
    if due_iso:
        properties["Due"] = {"date": {"start": due_iso}}

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": properties,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
