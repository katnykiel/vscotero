import pytest
from pathlib import Path
import sqlite3
import textwrap


@pytest.fixture
def temp_env(tmp_path: Path):
    bib = tmp_path / "library.bib"
    md_dir = tmp_path / "notes"
    db_path = tmp_path / "zotero.sqlite"
    md_dir.mkdir()

    bib.write_text(textwrap.dedent(r"""
    @article{smith2024example,
      title = {An Example Paper},
      author = {Smith, Alice and Doe, Bob},
      year = {2024},
      file = {/abs/path/to/example.pdf},
    }
    """
    ).strip())

    # create minimal sqlite db
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE itemAnnotations (parentItemID INTEGER, text TEXT, comment TEXT, color TEXT, pageLabel TEXT)")
        cur.execute("CREATE TABLE itemAttachments (itemID INTEGER, path TEXT)")
        cur.execute("INSERT INTO itemAttachments (itemID, path) VALUES (1, '/abs/path/to/example.pdf')")
        cur.execute("INSERT INTO itemAnnotations VALUES (1, 'Highlighted sentence', 'Interesting', '#ffd400', '3')")
        conn.commit()

    config_toml = tmp_path / "config.toml"
    config_toml.write_text(f"""
    [notes]
    bib_path = "{bib}"
    md_path = "{md_dir}"
    db_path = "{db_path}"
    """)
    return {
        "bib": bib,
        "md_dir": md_dir,
        "db": db_path,
        "config": config_toml,
        "root": tmp_path,
    }
