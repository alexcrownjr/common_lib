import os
import peewee


def database_connector_wrapper(**kwargs):
    """
    Create db instance from params.

    If required params are not provided, try to get them from env vars.
    """
    required_params_mapping = {
        'database': 'POSTGRES_DB',
        'user': 'POSTGRES_USER',
        'password': 'POSTGRES_PASSWORD',
        'host': 'POSTGRES_HOST',
        'port': 'POSTGRES_PORT'
    }

    default_params = {
        'autocommit': True,
        'autorollback': True
    }

    missing = set(required_params_mapping.keys()).difference(kwargs.keys())
    invalid_params = set(kwargs.keys()).difference(required_params_mapping.keys())

    # check provided params are enough to instantiate db connection
    for param in missing:
        kwargs[param] = os.environ[required_params_mapping[param]]

    # remove unsupported options
    [kwargs.pop(param) for param in invalid_params]

    kwargs.update(default_params)

    return peewee.PostgresqlDatabase(**kwargs)
