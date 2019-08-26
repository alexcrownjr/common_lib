"""
Peewee pytest plugin.
"""
import os
import importlib
import peewee
import psycopg2
import pytest

from .storage import database_connector_wrapper
from .storage import utils


class DatabaseManager:
    def __init__(
            self, database,
            user=os.environ['POSTGRES_USER'],
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT']
    ):
        """
        Initialize database for tests run.
        """
        self.user = user
        self.host = host
        self.port = port
        self.database = database
        self.password = os.environ['POSTGRES_PASSWORD']

    def _cursor_init(self):
        """
        Return postgresql cursor.
        """
        conn = psycopg2.connect(user=self.user, host=self.host, port=self.port, password=self.password)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = conn.cursor()
        self.connection = conn

    def create(self):
        try:
            self.cursor.execute(f'DROP DATABASE {self.database};')
        except Exception:
            pass
        self.cursor.execute(f'CREATE DATABASE {self.database};')

    def drop(self):
        """
        Drop database in postgresql.
        """
        # terminate all connections first while not allowing new connections
        pid_column = 'pid'
        with self.cursor as cur:
            cur.execute(
                'UPDATE pg_database SET datallowconn=false WHERE datname = %s;',
                (self.database, ))
            cur.execute(
                'SELECT pg_terminate_backend(pg_stat_activity.{})'
                'FROM pg_stat_activity '
                'WHERE pg_stat_activity.datname = %s;'.format(pid_column),
                (self.database, ))
            cur.execute(f'DROP DATABASE IF EXISTS {self.database};')

    def __enter__(self):
        self._cursor_init()
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()
        self.cursor.close()
        self.connection.close()


def pytest_load_initial_conftests(early_config, parser, args):
    # Register the marks
    early_config.addinivalue_line(
        "markers",
        "peewee_db(transaction=False): Mark the test as using "
        "the Peewee test database.  The *transaction* argument marks will "
        "allow you to use real transactions in the test",
    )


def pytest_collection_modifyitems(session, config, items):
    def get_order_number(test):
        marker_db = test.get_closest_marker('django_db')


@pytest.fixture(scope='session')
def models():
    loader_details = (
        importlib.machinery.SourceFileLoader,
        importlib.machinery.SOURCE_SUFFIXES
    )
    toolsfinder = importlib.machinery.FileFinder(os.environ["PROJECT_ROOT"], loader_details)
    specs = toolsfinder.find_spec("models")
    print(os.environ["PROJECT_ROOT"], specs, toolsfinder)
    models_module = specs.loader.load_module()
    ret = []
    for entity_name in dir(models_module):
        if entity_name == "BaseModel":
            continue
        entity = getattr(models_module, entity_name)
        if entity is peewee.Model:
            continue
        if isinstance(entity, peewee.ModelBase):
            ret.append(entity)
    return ret


@pytest.yield_fixture(scope='session')
def db(models):
    database = f"{__name__.split('.')[0]}_tests"
    with DatabaseManager(database) as dbm:
        _db = database_connector_wrapper(database=dbm.database, user=dbm.user, password=dbm.password)
        utils.create_db(_db, *models)
        yield _db


@pytest.yield_fixture(autouse=True)
def transactional_db(db):
    with db.transaction() as txn:
        yield txn
        txn.rollback()
