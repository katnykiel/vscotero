# core.py

import bibtexparser
import yaml
import os
from config import load_configuration
import logging


def get_bib_database(bibtex_file):
    """
    Read a BibTeX file and return a BibDatabase object

    Args:
        bibtex_file (str): The path to the BibTeX file.

    Returns:
        bib_database (BibDatabase): A BibDatabase object representing the BibTeX file.

    """

    # Check that there is a bib file at this location
    if not os.path.isfile(bibtex_file):
        raise FileNotFoundError("No BibTeX file found at {}".format(bibtex_file))

    # Read the bibtex file
    with open(bibtex_file, "r") as f:
        bibtex_str = f.read()

    # Configure the bibtexparser to allow for non-standard entry types
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False

    # Parse the bibtex file
    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

    return bib_database


def get_yaml_from_bib_entry(bib_entry):
    """
    Convert a BibTeX entry to YAML format.

    Args:
        bib_entry (dict): A dictionary representing a BibTeX entry.

    Returns:
        str: The YAML representation of the BibTeX entry.
    """

    # Convert the entry to yaml using yaml.dump
    yaml_str = yaml.dump(bib_entry, width=float("inf"))

    # TODO: add checks that we are getting the right YAML elements

    return yaml_str


def get_authors_from_bib_entry(bib_entry):
    """
    Get the authors from a BibTeX entry.

    Args:
        bib_entry (dict): A dictionary representing a BibTeX entry.

    Returns:
        list: A list of authors.
    """
    try:
        authors = bib_entry["author"].split(" and ")
        return authors
    except KeyError:
        return []


def make_markdown_file(yaml_str, authors, bib_entry, output_dir=""):
    """
    Create a markdown file for each BibTex entry. The markdown file will be named the same as the BibTex key.
    The markdown file will include the yaml representation of the BibTex entry.
    It will also include the names of each author enclosed in double square brackets.
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
        bib_entry["publisher"] = bib_entry["publisher"].replace("{", "").replace("}", "")

    # Check if the output directory exists
    if output_dir and os.path.isdir(output_dir):
        output_path = os.path.join(output_dir, f'{bib_entry["ID"]}.md')
    else:
        output_path = f'{bib_entry["ID"]}.md'

    # If there is a file there already then don't overwrite it
    if os.path.isfile(output_path):
        logging.debug(f"File already exists at {output_path}. Skipping.")
        return
    # Create the markdown file
    with open(output_path, "w") as f:
        author_string = ", ".join(f"[[{a}]]" for a in authors)

        doc = f"""---
{yaml_str}
---
{author_string}
"""
        f.write(doc)


if __name__ == "__main__":
    logging.basicConfig(filename="debug.log", level=logging.DEBUG)
