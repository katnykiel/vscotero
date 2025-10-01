import os
import logging

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
