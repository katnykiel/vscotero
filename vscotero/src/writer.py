from .bib import filter_bib_entry
import os
import yaml
import pandas as pd


class LitNote:
    def __init__(self, bib_entry, config):
        self.bib_entry = filter_bib_entry(bib_entry)
        self.note_path = os.path.join(
            config["notes"]["md_path"], f'{bib_entry["ID"]}.md'
        )
        self.colormap = config["notes"]["colormap"]
        self.annotations = None

    def get_yaml_str(self):
        return yaml.dump(self.bib_entry, width=float("inf"))

    def get_authors_str(self):
        try:
            authors = self.bib_entry["author"].split(" and ")
        except KeyError:
            authors = []
        return ", ".join(f"[[{a}]]" for a in authors)

    def get_annotations(self, annotation_df):
        annotations = annotation_df[annotation_df["bibID"] == self.bib_entry["ID"]]

        with pd.option_context("mode.chained_assignment", None):
            annotations["color"] = pd.Categorical(
                annotations["color"], categories=self.colormap.keys(), ordered=True
            )

        annotations = annotations.sort_values("color")

        # Group annotations by color
        grouped_annotations = annotations.groupby("color", observed=False)

        self.annotations = grouped_annotations

    def get_annotations_str(self):

        annotations_str = "## Annotations\n"

        for color, group in self.annotations:
            # Get the section heading based on color_map
            section_heading = self.colormap.get(color, "Other")

            # Write the section heading if the length of group is more than 1
            if len(group) < 1:
                continue

            annotations_str += f"\n### {section_heading}\n"

            for index, row in group.iterrows():
                text = row["text"]
                comment = row["comment"]
                pageLabel = row["pageLabel"]

                if comment is not None:
                    # Format the string
                    annotations_str += f"""
"{text}", pg. {pageLabel}

> {comment}
"""
                else:
                    # Format the string
                    annotations_str += f"""
"{text}", pg. {pageLabel}
"""

        return annotations_str

    def write_file(self):
        # Create the markdown file
        with open(self.note_path, "w") as f:
            doc = f"""---
{self.get_yaml_str()}
---
{self.get_authors_str()}

{self.get_annotations_str()}"""

            f.write(doc)
