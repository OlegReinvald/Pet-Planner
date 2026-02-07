from app.storage.local import append_note, load_notes


def test_append_and_load(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCAL_DATA_DIR", str(tmp_path))
    note = append_note({"title": "test", "type": "note"})
    notes = load_notes()
    assert note["title"] == "test"
    assert len(notes) == 1
