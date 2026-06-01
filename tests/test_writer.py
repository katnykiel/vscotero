from vscotero.bib import load_bib_database
from vscotero.annotations import load_annotations
from vscotero.writer import LiteratureNoteWriter


def _make_writer(temp_env, colormap=None):
    bib_db = load_bib_database(temp_env["bib"])
    entry = bib_db.entries[0]
    ann_df = load_annotations(temp_env["db"], bib_db)
    writer = LiteratureNoteWriter(entry, temp_env["md_dir"], colormap or {"#ffd400": "Insights"})
    writer.group_annotations(ann_df)
    return writer


def test_writer_creates_file(temp_env):
    writer = _make_writer(temp_env)
    writer.write()
    note_file = temp_env["md_dir"] / "smith2024example.md"
    assert note_file.is_file()
    content = note_file.read_text()
    assert "An Example Paper" in content
    assert "## Annotations" in content
    assert "Highlighted sentence" in content


def test_new_file_contains_block_fences(temp_env):
    writer = _make_writer(temp_env)
    writer.write()
    content = (temp_env["md_dir"] / "smith2024example.md").read_text()
    assert content.count("===") >= 2


def test_update_preserves_user_content(temp_env):
    writer = _make_writer(temp_env)
    writer.write()
    note_file = temp_env["md_dir"] / "smith2024example.md"
    # Append user content after the managed block
    note_file.write_text(note_file.read_text() + "\n## My Notes\n\nKeep this.\n")
    # Run write again (update mode, the default)
    writer.write()
    content = note_file.read_text()
    assert "## My Notes" in content
    assert "Keep this." in content


def test_overwrite_replaces_user_content(temp_env):
    writer = _make_writer(temp_env)
    writer.write()
    note_file = temp_env["md_dir"] / "smith2024example.md"
    note_file.write_text(note_file.read_text() + "\n## My Notes\n\nKeep this.\n")
    writer.write(overwrite=True)
    content = note_file.read_text()
    assert "## My Notes" not in content
