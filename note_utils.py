import os
from core import get_bib_database


def remove_md_files(md_path):
    """
    Removes all Markdown (.md) files from the specified directory.

    Args:
        md_path (str): The path to the directory.

    Returns:
        None
    """

    # Get a list of all files in the directory
    files = os.listdir(md_path)

    # Filter the list to include only MD files
    md_files = [file for file in files if file.endswith(".md")]

    # Check if there are any MD files
    if len(md_files) == 0:
        logging.debug("No .md files found in the directory.")
        return

    # Prompt the user for confirmation
    confirmation = input(
        f"Are you sure you want to remove {len(md_files)} .md files? (y/n): "
    )

    if confirmation.lower() == "y":
        # Remove the MD files
        for file in md_files:
            file_path = os.path.join(md_path, file)
            os.remove(file_path)
            print(f"Removed file: {file}")
    else:
        print("Operation cancelled.")


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
