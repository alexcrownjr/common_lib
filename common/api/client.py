import aiohttp
from aiohttp import ClientResponseError, ClientConnectionError
import logging


log = logging.getLogger(__name__)


class ApiClient:
    """
    Base api client.
    """
    def __init__(self, base_url=None, session=None, **session_kwargs):
        self._session = session or aiohttp.ClientSession(**session_kwargs)
        self._session_params = session_kwargs
        self._base_url = base_url

    @classmethod
    async def init(cls, base_url, **session_kwargs):
        """
        Initialize ApiClient asynchronously.
        """
        session = await aiohttp.ClientSession(**session_kwargs).__aenter__()
        self = cls(base_url, session, **session_kwargs)
        return self

    async def do_api_call(self, method, url, params=None):
        url = self._get_full_url(url)
        try:
            params = params or {}
            async with self._session.request(method, url, raise_for_status=True, params=params) as response:
                return await response.json()
        except (ClientResponseError, ClientConnectionError, BaseException) as ex:
            log.error("API error occurred for (%s, %s, %s): %s", method, url, params, ex)

    def _get_full_url(self, url):
        assert self._base_url
        base_url = self._base_url.rstrip('/')
        if url.startswith('/'):
            return base_url + url
        return f"{base_url}/{url}"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    def __exit__(self, *args, **kwargs):
        pass
