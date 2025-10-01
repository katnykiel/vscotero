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

    def yaml_front_matter(self) -> str:
        fm = yaml.safe_dump(self.entry, width=float("inf")).strip()
        return f"---\n{fm}\n---"

    def build_document(self) -> str:
        parts = [
            self.yaml_front_matter(),
            self.authors_str(),
            self.annotations_section(),
        ]
        return "\n\n".join(p for p in parts if p).rstrip() + "\n"

    def write(self):
        self.md_dir.mkdir(parents=True, exist_ok=True)
        self.note_path.write_text(self.build_document(), encoding="utf-8")


__all__ = ["LiteratureNoteWriter"]
