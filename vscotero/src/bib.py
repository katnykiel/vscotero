import os
import yaml
import bibtexparser


def get_bib_database(bibtex_path):
    """
    Read a BibTeX file and return a BibDatabase object

    Args:
        bibtex_path (str): The path to the BibTeX file.

    Returns:
        bib_database (BibDatabase): A BibDatabase object representing the BibTeX file.

    """

    # Check that there is a bib file at this location
    if not os.path.isfile(bibtex_path):
        raise FileNotFoundError("No BibTeX file found at {}".format(bibtex_path))

    # Read the bibtex file
    with open(bibtex_path, "r") as f:
        bibtex_str = f.read()

    # Configure the bibtexparser to allow for non-standard entry types
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False

    # Parse the bibtex file
    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

    return bib_database


def get_bibID_from_file(file_path, bib_database):
    """
    Get the bibID from the given file path.

    Args:
        file_path (str): The path to the file.
        bib_database (BibDatabase): The bib database containing the entries.

    Returns:
        str: The bibID if the file exists in the bib database, otherwise None.
    """

    # Search through the bib entries to find the file path
    bib_entries = bib_database.entries

    for entry in bib_entries:
        if "file" in entry:
            files = entry["file"].split(";")
            for file in files:
                if file.strip() == file_path:
                    return entry.get("ID")

    # If the file is not found, return None
    return None


def get_new_bib_entries(bib_database, md_path):
    """
    Get new bib entries by filtering out entries that have corresponding markdown files in the given path.

    Args:
        bib_database (BibDatabase): The original BibDatabase object.
        md_path (str): The path to the directory containing markdown files.

    Returns:
        BibDatabase: The filtered BibDatabase object without entries that have corresponding markdown files.
    """
    md_files = [file[:-3] for file in os.listdir(md_path) if file.endswith(".md")]

    filtered_bib_database = bib_database

    for entry in bib_database.entries.copy():
        if entry["ID"] in md_files:
            filtered_bib_database.entries.remove(entry)

    return filtered_bib_database


def filter_bib_entry(bib_entry):
    """
    Filter a BibTeX entry to remove unwanted fields.

    Args:
        bib_entry (dict): A dictionary representing a BibTeX entry.

    Returns:
        dict: The filtered BibTeX entry.
    """

    # If there is a / in the bib_entry["ID"] then remove the /
    bib_entry["ID"] = bib_entry["ID"].replace("/", "-")

    # Only take the last file, which may be split with ; or be a single file
    if "file" in bib_entry:
        bib_entry["file"] = bib_entry["file"].split(";")[-1]

    # Fix title by removing any curly braces
    if "title" in bib_entry:
        bib_entry["title"] = bib_entry["title"].replace("{", "").replace("}", "")

    # Do the same for publisher
    if "publisher" in bib_entry:
        bib_entry["publisher"] = (
            bib_entry["publisher"].replace("{", "").replace("}", "")
        )

    return bib_entry
