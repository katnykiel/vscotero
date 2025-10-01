import toml
from vscotero.src.writer import LitNote
from vscotero.src.bib import get_bib_database
from vscotero.src.annotations import get_annotations, load_database
from vscotero.src.utils import remove_md_files

# load your configuration file
config = toml.load("config.toml")

# set a colormap for your annotations
colormap = {
    "#e56eee": "Contributions",  # pink
    "#ffd400": "Insights",  # yellow
    "#ff6666": "Discrepancies",  # red
    "#a28ae5": "Methods",  # purple
    "#5fb236": "Gaps",  # green
    "#2ea8e5": "Supplemental",  # blue
}

config["notes"]["colormap"] = colormap

# remove old markdown files
# remove_md_files(config["notes"]["md_path"])

# load your bibtex database and annotations
bibDatabase = get_bib_database(config["notes"]["bib_path"])
annotation_df = get_annotations(config["notes"]["db_path"], bibDatabase)

# generate lit notes for each entry in your bibtex database
for bib_entry in bibDatabase.entries:
    note = LitNote(bib_entry, config)
    note.get_annotations(annotation_df)
    note.write_file()
