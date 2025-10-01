from __future__ import annotations

from pathlib import Path
import typer
from .config import NotesConfig
from . import __version__
from .bib import load_bib_database
from .annotations import load_annotations
from .writer import LiteratureNoteWriter

app = typer.Typer(help="VSCode + Zotero ingestion utility")


@app.callback()
def version_callback(
    version: bool = typer.Option(
        False,
        "--version",
        callback=lambda v: (_display_version() if v else None),
        is_eager=True,
        help="Show version and exit",
    ),
):  # pragma: no cover - Typer handles exit
    """Root callback to support --version early exit."""
    # Returning None keeps normal flow when --version not provided.
    return None


def _display_version():  # pragma: no cover - simple output
    typer.echo(f"vscotero {__version__}")
    raise typer.Exit()


def ingest_core(config_path: Path, clean: bool = False, limit: int | None = None, debug: bool = False) -> int:
    """Core ingestion logic. Returns number of notes written."""
    cfg = NotesConfig.load(config_path)
    cfg.validate()

    if clean:
        for f in cfg.md_path.glob("*.md"):
            f.unlink()
        typer.secho("Cleaned existing notes", fg=typer.colors.YELLOW)

    bib_db = load_bib_database(cfg.bib_path)
    ann_df = load_annotations(cfg.db_path, bib_db, debug=debug)

    count = 0
    for entry in bib_db.entries:
        writer = LiteratureNoteWriter(entry, cfg.md_path, cfg.colormap)
        writer.group_annotations(ann_df)
        writer.write()
        count += 1
        if limit is not None and count >= limit:
            break
    typer.secho(f"Wrote {count} notes to {cfg.md_path}", fg=typer.colors.GREEN)
    return count


@app.command("ingest")
def ingest_command(
    path: Path = typer.Option(..., "--path", "-p", help="Path to config.toml"),
    clean: bool = typer.Option(False, help="Remove existing .md files before writing"),
    limit: int | None = typer.Option(None, help="Limit number of notes"),
    debug: bool = typer.Option(False, help="Print debug info for unmatched annotations"),
):
    """Generate literature notes from Zotero bib + annotations."""
    ingest_core(path, clean=clean, limit=limit, debug=debug)


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
