from fastapi import APIRouter, Request

from app.services.notion import create_note
from app.services.parser import parse_note
from app.services.telegram import send_message

router = APIRouter()


@router.post("/telegram")
async def telegram_webhook(request: Request):
    payload = await request.json()
    message = payload.get("message") or payload.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message.get("text")
    if not text:
        return {"ok": True}

    parsed = parse_note(text)
    create_note(parsed.title, parsed.note_type, parsed.due, str(chat_id))

    send_message(chat_id, f"Сохранено: {parsed.title}")
    return {"ok": True}
