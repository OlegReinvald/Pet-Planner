# Pet-Planner

Telegram бот для умных заметок с хранением в Notion.

## MVP
- Приём сообщений из Telegram (webhook)
- Парсинг типа заметки и даты/времени
- Запись в Notion
- Напоминания по времени

## Стек
- Python 3.11+
- FastAPI
- Notion API
- APScheduler (напоминания)

## Структура
```
app/
  api/            # webhook и ручки API
  services/       # Notion, Telegram, парсинг
  models/         # Pydantic модели
  utils/          # утилиты
  main.py         # вход

tests/
```

## Запуск (черновик)
```
uvicorn app.main:app --reload
```

## Переменные окружения
- TELEGRAM_BOT_TOKEN
- NOTION_TOKEN
- NOTION_DATABASE_ID
- WEBHOOK_SECRET (опционально)

## Roadmap
- [ ] Автоклассификация заметок
- [ ] Улучшенный парсинг дат
- [ ] Дайджест дня
- [ ] Голосовые заметки
