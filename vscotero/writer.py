from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml
from .bib import filter_bib_entry


class LiteratureNoteWriter:
    def __init__(self, bib_entry: dict, md_dir: Path, colormap: dict[str, str]):
        self.entry = filter_bib_entry(bib_entry)
        self.md_dir = md_dir
        self.colormap = colormap
        self.annotations_grouped = None
        self.item_notes = None

    @property
    def note_path(self) -> Path:
        return self.md_dir / f"{self.entry['ID']}.md"

    def authors_str(self) -> str:
        raw = self.entry.get("author", "")
        if not raw:
            return ""
        authors = [a.strip() for a in raw.split(" and ") if a.strip()]
        return ", ".join(f"[[{a}]]" for a in authors)

    def group_annotations(self, annotation_df: pd.DataFrame):
        subset = annotation_df[annotation_df["bibID"] == self.entry["ID"]].copy()
        if subset.empty:
            self.annotations_grouped = []
            return
        subset["color"] = pd.Categorical(
            subset["color"], categories=list(self.colormap.keys()), ordered=True
        )
        subset = subset.sort_values("color")
        self.annotations_grouped = list(subset.groupby("color", observed=False))

    def set_item_notes(self, item_notes_df: pd.DataFrame):
        """Set item notes for this entry."""
        subset = item_notes_df[item_notes_df["bibID"] == self.entry["ID"]].copy()
        if subset.empty:
            self.item_notes = []
        else:
            self.item_notes = subset[["title", "note"]].to_dict("records")

    def annotations_section(self) -> str:
        if self.annotations_grouped is None:
            return "## Annotations\n"
        out = ["## Annotations"]
        for color, group in self.annotations_grouped:
            if group.empty:
                continue
            heading = self.colormap.get(color, "Other")
            out.append(f"### {heading}")
            for _, row in group.iterrows():
                text = row["text"]
                page = row["pageLabel"]
                comment = row["comment"]
                if comment:
                    out.append(f'"{text}", pg. {page}\n\n> {comment}')
                else:
                    out.append(f'"{text}", pg. {page}')
        return "\n\n".join(out) + "\n"

    def item_notes_section(self) -> str:
        """Format item notes as a section at the bottom of the document."""
        if self.item_notes is None or not self.item_notes:
            return ""
        out = ["## Notes"]
        for note_dict in self.item_notes:
            title = note_dict.get("title", "").strip()
            note = note_dict.get("note", "").strip()
            if title:
                out.append(f"### {title}")
                # Remove title from note content if it appears at the start
                if note and note.startswith(title):
                    note = note[len(title):].strip()
                if note:
                    out.append(note)
            elif note:
                out.append(note)
        return "\n\n".join(out) + "\n"

    BLOCK_FENCE = "==="

    def yaml_front_matter(self) -> str:
        fm = yaml.safe_dump(self.entry, width=float("inf")).strip()
        return f"---\n{fm}\n---"

    def build_managed_block(self) -> str:
        """Build the auto-generated content that lives inside the === fences."""
        parts = [
            self.authors_str(),
            self.annotations_section(),
            self.item_notes_section(),
        ]
        inner = "\n\n".join(p for p in parts if p).rstrip()
        return f"{self.BLOCK_FENCE}\n\n{inner}\n\n{self.BLOCK_FENCE}"

    def build_document(self) -> str:
        parts = [
            self.yaml_front_matter(),
            self.build_managed_block(),
        ]
        return "\n\n".join(p for p in parts if p).rstrip() + "\n"

    def update_document(self, existing: str) -> str:
        """Return updated content: replaces YAML front matter and managed block,
        preserving everything else in the file."""
        import re

        new_yaml = self.yaml_front_matter()
        new_block = self.build_managed_block()

        # Replace YAML front matter (must be at start of file)
        yaml_pattern = re.compile(r"^---\n.*?\n---", re.DOTALL)
        if yaml_pattern.match(existing):
            updated = yaml_pattern.sub(lambda _: new_yaml, existing, count=1)
        else:
            # No existing front matter — prepend it
            updated = new_yaml + "\n\n" + existing

        # Replace managed block if present, otherwise append it
        fence = re.escape(self.BLOCK_FENCE)
        block_pattern = re.compile(
            r"^" + fence + r"\n.*?\n" + fence + r"$",
            re.DOTALL | re.MULTILINE,
        )
        if block_pattern.search(updated):
            updated = block_pattern.sub(lambda _: new_block, updated, count=1)
        else:
            updated = updated.rstrip() + "\n\n" + new_block + "\n"

        return updated.rstrip() + "\n"

    def write(self, overwrite: bool = False):
        self.md_dir.mkdir(parents=True, exist_ok=True)
        if not overwrite and self.note_path.exists():
            existing = self.note_path.read_text(encoding="utf-8")
            self.note_path.write_text(self.update_document(existing), encoding="utf-8")
        else:
            self.note_path.write_text(self.build_document(), encoding="utf-8")


__all__ = ["LiteratureNoteWriter"]
