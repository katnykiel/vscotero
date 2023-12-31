# core.py

import bibtexparser
import yaml
import os
from config import load_configuration

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
    yaml_str = yaml.dump(bib_entry)

    # TODO: add checks that we are getting the right YAML elements

    # Check to see if we get the right YAML elements

    return yaml_str


def loop_through_bib_database(bib_database):
    """
    Loop through the entries in the given BibTeX database and perform some operation on each entry.

    Args:
        bib_database (BibDatabase): The BibTeX database to loop through.

    Returns:
        None
    """
    for entry in bib_database.entries:
        get_yaml_from_bib_entry(entry)


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

    # Check if the output directory exists
    if output_dir and os.path.isdir(output_dir):
        output_path = os.path.join(output_dir, f'{bib_entry["ID"]}.md')
    else:
        output_path = f'{bib_entry["ID"]}.md'

    # Create the markdown file
    with open(output_path, "w") as f:
        author_string = ", ".join(f"[[{a}]]" for a in authors)

        doc = f"""---
{yaml_str}
---
{author_string}
"""
        f.write(doc)

