# vsco-tero

import bibtexparser
import yaml
import os


def get_bib_database(bibtex_file):
    """
    Read a BibTeX file and parse it into a BibDatabase object.

    Args:
        bibtex_file (str): The path to the BibTeX file.

    Returns:
        BibDatabase: The parsed BibDatabase object.

    """
    # Read the bibtex file
    with open(bibtex_file, 'r') as f:
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
    # Convert the entry to yaml
    yaml_str = yaml.dump(bib_entry)

    yaml_str = yaml_str.replace('{', '').replace('}', '')

    print(yaml_str)

    return yaml_str

def loop_through_bib_database(bib_database):
    
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
        authors = bib_entry['author'].split(' and ')
        print(authors)
        return authors
    except KeyError:
        print('No authors found')
        return []

def make_markdown_file(yaml_str, authors, bib_entry):
    """
    Create a markdown file for each BibTex entry. The markdown file will be named the same as the BibTex key.
    The markdown file will include the yaml representation of the BibTex entry.
    It will also include the names of each author enclosed in double square brackets.
    """

    # Create the markdown file
    with open(f'{bib_entry["ID"]}.md', 'w') as f:
        
        author_string = ", ".join(f"[[{a}]]" for a in authors)
        
        doc = f"""---
{yaml_str}
---
{author_string}
"""
        f.write(doc)

test_bibtex_file = '/Users/aerith/warlock/vsco-tero/tests/test.bib'

bib_database = get_bib_database(test_bibtex_file)

loop_through_bib_database(bib_database)

for bib_entry in bib_database.entries:
    yaml_str = get_yaml_from_bib_entry(bib_entry)
    authors = get_authors_from_bib_entry(bib_entry)
    make_markdown_file(yaml_str, authors, bib_entry)