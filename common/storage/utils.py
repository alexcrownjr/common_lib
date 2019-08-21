"""
Storage utils.
"""
from misc.storage import db


def create_db(*args):
    """
    Create db tables from models
    """
    db.create_tables(args)


def delete_db(*args):
    """
    Drops database tables.
    """
    db.drop_tables(args)


def recreate_db():
    """
    Drop existing DB and create new one.
    """
    delete_db()
    create_db()
