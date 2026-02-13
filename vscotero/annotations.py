from __future__ import annotations

import sqlite3
import re
import html
import pandas as pd
from pathlib import Path
import tempfile
import shutil
import os
from contextlib import suppress
from .bib import bib_id_from_attachment_path, _normalize_path

ANNOTATIONS_QUERY = """
SELECT ia.parentItemID,
       ia.text,
       ia.comment,
       ia.color,
       ia.pageLabel,
       at.path AS attachment_path
FROM itemAnnotations ia
JOIN itemAttachments at ON ia.parentItemID = at.itemID
"""

ITEM_NOTES_QUERY = """
SELECT n.parentItemID,
       n.note,
       n.title,
       at.path AS attachment_path
FROM itemNotes n
JOIN itemAttachments at ON n.parentItemID = at.parentItemID
"""


def _copy_sqlite_file(src: Path) -> Path:
    """Copy the sqlite database to a temporary file to avoid locking issues.

    Returns the path to the temporary copy (caller is responsible for deletion).
    """
    tmp_dir = tempfile.gettempdir()
    # NamedTemporaryFile(delete=False) to allow sqlite to open it after close
    with tempfile.NamedTemporaryFile(prefix="vscotero_db_", suffix=".sqlite", dir=tmp_dir, delete=False) as tf:
        tmp_path = Path(tf.name)
    shutil.copy2(src, tmp_path)
    return tmp_path


def _strip_html(text: str) -> str:
    """Strip HTML tags and decode entities from text, preserving newlines."""
    if not text:
        return text
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up multiple spaces on same line, but preserve newlines
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove leading/trailing whitespace on each line
    lines = [line.strip() for line in text.split('\n')]
    # Remove empty lines but keep structure
    text = '\n'.join(lines).strip()
    return text


def load_annotations(db_path: Path, bib_db, use_copy: bool = True, debug: bool = False) -> pd.DataFrame:
    """Load annotations into a DataFrame.

    If the Zotero database is locked by a running Zotero instance, copying the file first
    avoids 'database is locked' errors. Set use_copy=False to read directly.
    """
    db_path = db_path.expanduser()
    working_path: Path = db_path

    if use_copy:
        try:
            working_path = _copy_sqlite_file(db_path)
        except Exception:
            # Fall back to direct path if copy fails; will raise below if unusable
            working_path = db_path

    try:
        # Use read-only URI if possible (safer); fallback if error
        uri = f"file:{working_path}?mode=ro" if working_path.is_file() else str(working_path)
        try:
            conn = sqlite3.connect(uri, uri=True)
        except sqlite3.OperationalError:
            conn = sqlite3.connect(str(working_path))
        with conn:
            df = pd.read_sql_query(ANNOTATIONS_QUERY, conn)
    finally:
        if use_copy and working_path != db_path:
            with suppress(OSError):
                os.remove(working_path)

    # Resolve bib IDs
    resolutions = []
    for p in df["attachment_path"]:
        resolutions.append(bib_id_from_attachment_path(p, bib_db))
    df["bibID"] = resolutions

    if debug:
        unmatched = df[df["bibID"].isna()]["attachment_path"].tolist()
        if unmatched:
            print("[vscotero] Unmatched attachment paths (showing up to 10):")
            for up in unmatched[:10]:
                print("  -", up, "->", _normalize_path(up))
    # Drop rows we cannot resolve
    df = df.dropna(subset=["bibID"])
    return df[["parentItemID", "text", "comment", "color", "pageLabel", "bibID"]]


def load_item_notes(db_path: Path, bib_db, use_copy: bool = True) -> pd.DataFrame:
    """Load item notes into a DataFrame and match them to bibIDs.

    Item notes are standalone notes attached to library items (documents).
    """
    db_path = db_path.expanduser()
    working_path: Path = db_path

    if use_copy:
        try:
            working_path = _copy_sqlite_file(db_path)
        except Exception:
            working_path = db_path

    try:
        uri = f"file:{working_path}?mode=ro" if working_path.is_file() else str(working_path)
        try:
            conn = sqlite3.connect(uri, uri=True)
        except sqlite3.OperationalError:
            conn = sqlite3.connect(str(working_path))
        with conn:
            df = pd.read_sql_query(ITEM_NOTES_QUERY, conn)
    finally:
        if use_copy and working_path != db_path:
            with suppress(OSError):
                os.remove(working_path)

    if df.empty:
        return pd.DataFrame(columns=["parentItemID", "note", "title", "bibID"])

    # Strip HTML from notes and titles
    df["note"] = df["note"].apply(_strip_html)
    df["title"] = df["title"].apply(_strip_html)

    # Resolve bib IDs using the attachment paths
    resolutions = []
    for p in df["attachment_path"]:
        resolutions.append(bib_id_from_attachment_path(p, bib_db))
    df["bibID"] = resolutions
    
    # Drop rows we cannot resolve
    df = df.dropna(subset=["bibID"])
    return df[["parentItemID", "note", "title", "bibID"]]


__all__ = ["load_annotations", "load_item_notes", "ANNOTATIONS_QUERY", "ITEM_NOTES_QUERY"]
