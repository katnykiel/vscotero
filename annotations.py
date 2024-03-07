import os
import sqlite3
from peewee import *
import pandas as pd
import shutil
import warnings
import logging
from note_utils import get_bibID_from_file
from config import load_configuration


def copy_database_file(source_path):
    """
    Copy the database file from the source path to a new destination path.

    Args:
        source_path (str): The path of the source database file.

    Returns:
        str: The path of the copied database file.
    """
    destination_path = source_path + ".copy"
    shutil.copy2(source_path, destination_path)
    return destination_path


def load_database(db_path=os.path.expanduser("~/Zotero/zotero.sqlite")):
    """
    Load the Zotero database from the specified path.

    Args:
        db_path (str, optional): The path to the Zotero database file. Defaults to the user's Zotero directory.

    Returns:
        SqliteDatabase: The loaded database object.
    """
    db_path_copy = copy_database_file(db_path)
    db = SqliteDatabase(db_path_copy)
    return db


# Load the database
db = load_database()


class ItemAttachments(Model):
    """
    Represents the attachments for an item.

    Attributes:
        itemID (int): The ID of the item (primary key).
        path (str): The path of the attachment.
    """

    itemID = AutoField(primary_key=True)
    path = TextField()

    class Meta:
        database = db
        table_name = "itemAttachments"


class ItemAnnotations(Model):
    """
    Represents annotations for an item.
    """

    parentItemID = AutoField(primary_key=True)
    text = TextField()
    comment = TextField()
    color = TextField()
    pageLabel = TextField()

    class Meta:
        database = db
        table_name = "itemAnnotations"


def get_table_data(db):
    """
    Retrieves table data from the database and returns it as a pandas DataFrame.

    Returns:
        pandas.DataFrame: The table data.
    """
    db.connect()

    annotations = ItemAnnotations.select()
    data = []
    for annotation in annotations:
        attachment = ItemAttachments.get(
            ItemAttachments.itemID == annotation.parentItemID
        )
        row = {
            "parentItemID": annotation.parentItemID,
            "text": annotation.text,
            "comment": annotation.comment,
            "color": annotation.color,
            "pageLabel": annotation.pageLabel,
            "bibID": attachment.path,
        }
        data.append(row)

    db.close()
    df = pd.DataFrame(data)
    return df


def filter_table_data(df, bib_database):
    """
    Filter table data by removing annotations with incorrect paths and stripping out bibID from path.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the table data.
        bib_database (BibDatabase): The BibDatabase object containing the correct bibID information.

    Returns:
        pandas.DataFrame: The filtered DataFrame with annotations removed and bibID stripped.
    """
    filtered_df = df.copy()

    # Updatet the bibID column with the correct path
    filtered_df["bibID"] = filtered_df["bibID"].apply(
        lambda x: get_bibID_from_file(x, bib_database)
    )

    return filtered_df


def append_to_md_file(
    df,
    md_path,
    rewrite_annotations=True,
    colormap={
        "#e56eee": "Contributions",
        "#ffd400": "Insights",
        "#ff6666": "Discrepancies",
        "#a28ae5": "Methods",
        "#5fb236": "Gaps",
        "#2ea8e5": "Supplemental",
    },
):
    unique_bibIDs = df["bibID"].unique()

    for bibID in unique_bibIDs:
        annotations = df[df["bibID"] == bibID]

        # Check if the file exists
        file_path = f"{md_path}/{bibID}.md"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                lines = file.readlines()

                if rewrite_annotations and ("## Annotations\n" in lines):
                    # Get the annotations section
                    logging.debug(
                        f"Annotations section for {bibID} already exists. Rewriting annotations."
                    )
                    lines = lines[: lines.index("## Annotations\n") - 1]

            with open(file_path, "w") as file:
                # Write the lines back to the file
                file.writelines(lines)

                # Define an annotations section
                file.write("\n## Annotations\n")

                warnings.simplefilter(
                    action="ignore", category=pd.errors.PerformanceWarning
                )

                with pd.option_context("mode.chained_assignment", None):
                    annotations["color"] = pd.Categorical(
                        annotations["color"], categories=colormap.keys(), ordered=True
                    )

                annotations = annotations.sort_values("color")

                # Group annotations by color
                grouped_annotations = annotations.groupby("color", observed=False)

                for color, group in grouped_annotations:
                    # Get the section heading based on color_map
                    section_heading = colormap.get(color, "Other")

                    # Write the section heading if the length of group is more than 1
                    if len(group) >= 1:
                        file.write(f"\n### {section_heading}\n")

                    for index, row in group.iterrows():
                        text = row["text"]
                        comment = row["comment"]
                        pageLabel = row["pageLabel"]

                        if comment is not None:
                            # Format the string
                            formatted_string = f"""
"{text}", pg. {pageLabel}

> {comment}
"""
                        else:
                            # Format the string
                            formatted_string = f"""
"{text}", pg. {pageLabel}
"""

                        # Append the formatted string to the Markdown file
                        file.write(formatted_string)


if __name__ == "__main__":
    logging.basicConfig(filename="debug.log", level=logging.DEBUG)
