# vsco-tero

import bibtexparser
import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


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

    return yaml_str


def test_functions():
    """
    Test the get_bib_database and get_yaml_from_bib_entry functions.
    """

    # Get the BibDatabase object
    entries = get_bib_database("tests/test.bib")

    # Print the YAML representation of each BibTeX entry
    for entry in entries.entries:
        print(get_yaml_from_bib_entry(entry))


test_functions()


def loop_through_bib_database(bib_database):
    for entry in bib_database.entries:
        get_yaml_from_bib_entry(entry)


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has been modified")
            # TODO: Add script executable here


def check(watchdog_path):
    path = watchdog_path
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# check()
