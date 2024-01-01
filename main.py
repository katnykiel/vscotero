from config import load_configuration
from core import (
    get_bib_database,
    get_yaml_from_bib_entry,
    get_authors_from_bib_entry,
    make_markdown_file,
)

from annotations import (
    load_database,
    get_table_data,
    filter_table_data,
    append_to_md_file,
)

from note_utils import remove_md_files, get_new_bib_entries


def generate_lit_notes(bibtex_file, md_path):
    """
    Retrieves literature notes from a BibTeX file and generates markdown files.

    Args:
        bibtex_file (str): The path to the BibTeX file.
        md_path (str): The path to the directory where the markdown files will be generated.

    Returns:
        None
    """
    bib_database = get_bib_database(bibtex_file)

    for bib_entry in bib_database.entries:
        yaml_str = get_yaml_from_bib_entry(bib_entry)
        authors = get_authors_from_bib_entry(bib_entry)
        make_markdown_file(yaml_str, authors, bib_entry, md_path)


def update_bibnotes(bibtex_file, md_path):
    """
    Update the bibliography notes by extracting new entries from a BibTeX file and generating corresponding markdown files.

    Parameters:
    - bibtex_file (str): The path to the BibTeX file.
    - md_path (str): The path to the directory where the markdown files will be generated.

    Returns:
    None
    """
    bib_database = get_bib_database(bibtex_file)
    new_bib_database = get_new_bib_entries(bib_database, md_path)

    for bib_entry in new_bib_database.entries:
        yaml_str = get_yaml_from_bib_entry(bib_entry)
        authors = get_authors_from_bib_entry(bib_entry)
        make_markdown_file(yaml_str, authors, bib_entry, md_path)


def update_annotations(md_path):
    """
    Update annotations in a Markdown file with filtered data from a database.

    Args:
        md_path (str): The path to the Markdown file.

    Returns:
        None
    """
    db = load_database()
    df = get_table_data(db)
    filtered_df = filter_table_data(df)
    append_to_md_file(filtered_df, md_path)


if __name__ == "__main__":
    bibtex_file, pdf_path, openai_api_key, md_path = load_configuration()
    # remove_md_files(md_path)
    # generate_lit_notes(bibtex_file, md_path)
    update_bibnotes(bibtex_file, md_path)
    update_annotations(md_path)
