"""
Storage utils.
"""


def get_db_from_models(models):
    dbs = set([model._meta.db for model in models])
    if len(list(dbs)) == 1:
        return dbs.pop()
    raise Exception("Multiple databases are not supported!")


def create_db(*args, db=None):
    """
    Create db tables from models
    """
    if not db:
        db = get_db_from_models(args)
    db.create_tables(args)


def delete_db(*args, db=None):
    """
    Drops database tables.
    """
    if not db:
        db = get_db_from_models(args)
    db.drop_tables(args)


def recreate_db():
    """
    Drop existing DB and create new one.
    """
    delete_db()
    create_db()
