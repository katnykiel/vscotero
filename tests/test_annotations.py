from vscotero.bib import load_bib_database
from vscotero.annotations import load_annotations
import sqlite3


def test_load_annotations(temp_env):
    bib_db = load_bib_database(temp_env["bib"])
    df = load_annotations(temp_env["db"], bib_db)
    assert len(df) == 1
    row = df.iloc[0]
    assert row["text"] == "Highlighted sentence"
    assert row["bibID"] == "smith2024example"


def test_load_annotations_when_locked(temp_env):
    """Ensure we can still read when the original DB is 'locked' by another connection."""
    # Open a transaction and keep it open to simulate a lock
    conn = sqlite3.connect(temp_env["db"])
    cur = conn.cursor()
    cur.execute("BEGIN EXCLUSIVE")
    bib_db = load_bib_database(temp_env["bib"])
    # Should succeed because we copy first
    df = load_annotations(temp_env["db"], bib_db, use_copy=True)
    assert not df.empty
    conn.rollback()
    conn.close()
