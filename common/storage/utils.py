"""
Storage utils.
"""
from commo.storage import db


def create_db(db, *args):
    """
    Create db tables from models
    """
    db.create_tables(args)


def delete_db(db, *args):
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
