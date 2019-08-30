"""
Exchange services base.
"""
import os
import json
import logging

from common.exceptions import ImproperlyConfigured


log = logging.getLogger(__name__)


class ExchangeServiceBase:
    """
    Exchange base class.
    """
    client = None
    prefix = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.prefix:
            raise ImproperlyConfigured("Exchange-specific prefix must be set")
        if self.client is None:
            raise Exception("Improperly configured service client")

    @classmethod
    async def _init(cls, credentials=False):
        """
        By default exchange credentials are taken from env variables.
        """
        if credentials:
            cls.client = await cls.create_client_from_credentials()
        else:
            cls.client = await cls.create_client_from_env()

    @classmethod
    async def init(cls, loop=None, credentials=False):
        """
        Initialize exchange asynchronous factory function.
        Use it to instantiate Exchange with client with proper credentials.
        Example:
            class MyExchangeService(ExchangeServiceBase):
                prefix = 'my'
            my_service = await MyExchangeService.init(loop, credentials=True)
        """
        await cls._init(credentials)
        return cls()

    @classmethod
    async def create_client_from_credentials(cls):
        """
        Try to search for credentials.json file in project root, falls back to current directory (file run from).
        """
        with open(f"{os.environ.get('PROJECT_ROOT', '.')}/credentials.json", "r") as secret_file:
            try:
                data = json.load(secret_file)
                key, secret = data.values()
            except (json.JSONDecodeError, ValueError) as ex:
                log.error("Failed to fetch data from credentials.json file. Error: %s", ex)
        return await cls.create_client(key, secret)

    @classmethod
    async def create_client_from_env(cls):
        """
        Try to search for prefixed key/secret env variables.
        """
        prefix = cls.prefix.upper()
        key = os.environ[f'{prefix}_KEY']
        secret = os.environ[f'{prefix}_SECRET']
        return await cls.create_client(key, secret)

    @staticmethod
    async def create_client(key, secret):
        raise NotImplementedError()
