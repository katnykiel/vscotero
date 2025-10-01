from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import toml

_DEFAULT_COLORMAP = {
    "#e56eee": "Contributions",
    "#ffd400": "Insights",
    "#ff6666": "Discrepancies",
    "#a28ae5": "Methods",
    "#5fb236": "Gaps",
    "#2ea8e5": "Supplemental",
}


@dataclass
class NotesConfig:
    bib_path: Path
    md_path: Path
    db_path: Path
    colormap: dict[str, str] = field(default_factory=lambda: _DEFAULT_COLORMAP)

    @classmethod
    def load(cls, config_path: Path) -> "NotesConfig":
        data = toml.load(config_path)
        notes = data.get("notes", {})
        return cls(
            bib_path=Path(notes.get("bib_path", "")).expanduser(),
            md_path=Path(notes.get("md_path", "")).expanduser(),
            db_path=Path(notes.get("db_path", "")).expanduser(),
            colormap=notes.get("colormap") or _DEFAULT_COLORMAP,
        )

    def validate(self):
        missing: list[str] = []
        if not self.bib_path.is_file():
            missing.append(f"bib_path: {self.bib_path}")
        if not self.db_path.is_file():
            missing.append(f"db_path: {self.db_path}")
        if not self.md_path.exists():
            self.md_path.mkdir(parents=True, exist_ok=True)
        if missing:
            raise FileNotFoundError("Missing required file(s): " + ", ".join(missing))


__all__ = ["NotesConfig", "_DEFAULT_COLORMAP"]
