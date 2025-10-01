from __future__ import annotations

from pathlib import Path
import bibtexparser
import os
from functools import lru_cache


def load_bib_database(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"No BibTeX file at {path}")
    with path.open("r") as fh:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        return bibtexparser.loads(fh.read(), parser=parser)


def filter_bib_entry(entry: dict) -> dict:
    entry = dict(entry)  # shallow copy
    if "ID" in entry:
        entry["ID"] = entry["ID"].replace("/", "-")
    if "file" in entry:
        entry["file"] = entry["file"].split(";")[-1]
    for k in ("title", "publisher"):
        if k in entry:
            entry[k] = entry[k].replace("{", "").replace("}", "")
    return entry


@lru_cache(maxsize=2048)
def _normalize_path(p: str) -> str:
    # Remove surrounding braces or quotes, expand user, resolve relative artifacts
    p = p.strip().strip('{}"')
    # Split on ':' if Zotero appends type metadata (e.g., 'pdf:...')
    if ":" in p and not p.startswith("/"):
        # heuristic: keep rightmost path-like segment containing a slash
        parts = p.split(":")
        for candidate in reversed(parts):
            if "/" in candidate or candidate.endswith('.pdf'):
                p = candidate
                break
    p = os.path.expanduser(p)
    # We do not resolve symlinks (avoid hitting user FS unnecessarily); lowercase for matching
    return p.replace("\\", "/").rstrip().lower()


def bib_id_from_attachment_path(attachment_path: str, bib_db) -> str | None:
    if not attachment_path:
        return None
    norm_target = _normalize_path(attachment_path)

    # Pre-build normalized file list for each entry
    for entry in bib_db.entries:
        file_field = entry.get("file")
        if not file_field:
            continue
        # BibTeX export may include multiple files separated by ';'
        files = [f.strip() for f in file_field.split(";") if f.strip()]
        norm_files = [_normalize_path(f) for f in files]
        if norm_target in norm_files:
            return entry.get("ID")

        # Fallback: compare just basenames if full paths differ (user moved library)
        target_base = os.path.basename(norm_target)
        if target_base and any(os.path.basename(f) == target_base for f in norm_files):
            return entry.get("ID")
    return None


def iter_new_entries(bib_db, existing_ids: set[str]):
    for e in bib_db.entries:
        if e.get("ID") not in existing_ids:
            yield e


__all__ = [
    "load_bib_database",
    "filter_bib_entry",
    "bib_id_from_attachment_path",
    "iter_new_entries",
]
