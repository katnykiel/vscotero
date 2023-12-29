# vsco-tero

import bibtexparser
import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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

    print(yaml_str)

    return yaml_str

def loop_through_bib_database(bib_database):
    
    for entry in bib_database.entries:
        get_yaml_from_bib_entry(entry)



class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f'File {event.src_path} has been modified')
            # TODO: Add script executable here
            

def main(watchdog_path):
    if __name__ == "main":
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