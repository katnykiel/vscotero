import os
import sqlite3
from peewee import *
import pandas as pd
import shutil
import warnings
import logging
from .bib import get_bibID_from_file
import toml

config = toml.load("config.toml")


def get_annotations(db_path, bibDatabase):
    """
    Get the annotations from the Zotero database.

    Args:
        db_path (str): The path to the Zotero database file.
        bibDatabase (BibDatabase): The BibDatabase object containing the correct bibID information.

    Returns:
        pandas.DataFrame: A DataFrame containing the annotations.
    """
    db = load_database(db_path)
    df = get_table_data(db)
    df = filter_table_data(df, bibDatabase)
    return df


def copy_database_file(db_path):
    """
    Copy the database file from the source path to a new destination path.

    Args:
        db_path (str): The path of the source database file.

    Returns:
        str: The path of the copied database file.
    """
    destination_path = db_path + ".copy"
    shutil.copy2(db_path, destination_path)
    return destination_path


def load_database(db_path):
    """
    Load the Zotero database from the specified path.

    Args:
        db_path (str, optional): The path to the Zotero database file. Defaults to the user's Zotero directory.

    Returns:
        SqliteDatabase: The loaded database object.
    """
    db_path = os.path.expanduser(db_path)
    db_path_copy = copy_database_file(db_path)
    db = SqliteDatabase(db_path_copy)
    return db


db = load_database(config["notes"]["db_path"])


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


def filter_table_data(df, bibDatabase):
    """
    Filter table data by removing annotations with incorrect paths and stripping out bibID from path.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the table data.
        bibDatabase (BibDatabase): The BibDatabase object containing the correct bibID information.

    Returns:
        pandas.DataFrame: The filtered DataFrame with annotations removed and bibID stripped.
    """
    filtered_df = df.copy()

    # Updatet the bibID column with the correct path
    filtered_df["bibID"] = filtered_df["bibID"].apply(
        lambda x: get_bibID_from_file(x, bibDatabase)
    )

    return filtered_df
