from app.services.parser import parse_note


def test_parse_note_type_and_due():
    note = parse_note("Завтра 10:00 эндокринолог")
    assert note.title
    assert note.note_type in {"task", "note", "idea", "buy"}


def test_commands():
    note = parse_note("/task Сделать отчёт завтра")
    assert note.note_type == "task"
    assert note.title.lower().startswith("сделать")


def test_default_due_task():
    note = parse_note("/task Сделать отчёт")
    assert note.note_type == "task"
    assert note.due is not None


def test_parse_mixed_text_date():
    note = parse_note("test завтра")
    assert note.due is not None
