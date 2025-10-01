from vscotero.bib import load_bib_database
from vscotero.annotations import load_annotations
from vscotero.writer import LiteratureNoteWriter


def test_writer_creates_file(temp_env):
    bib_db = load_bib_database(temp_env["bib"])
    entry = bib_db.entries[0]
    ann_df = load_annotations(temp_env["db"], bib_db)
    writer = LiteratureNoteWriter(entry, temp_env["md_dir"], {"#ffd400": "Insights"})
    writer.group_annotations(ann_df)
    writer.write()
    note_file = temp_env["md_dir"] / "smith2024example.md"
    assert note_file.is_file()
    content = note_file.read_text()
    assert "An Example Paper" in content
    assert "## Annotations" in content
    assert "Highlighted sentence" in content
