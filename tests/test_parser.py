from app.services.parser import parse_note


def test_parse_note_type_and_due():
    note = parse_note("Завтра 10:00 эндокринолог")
    assert note.title
    assert note.note_type in {"task", "note", "idea", "buy"}
