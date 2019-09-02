from binance import AsyncClient, BinanceSocketManager

from .base import ExchangeServiceBase


class BinanceService(ExchangeServiceBase):
    """
    Binance exchange service.
    """
    socket_manager = None
    prefix = 'binance'

    def __init__(self, socket_manager=None, client=None):
        self.client = client
        self._socket_manager = socket_manager
        super(BinanceService, self).__init__()

    @classmethod
    async def init(cls, loop=None, credentials=False, **kwargs):
        """
        Initialize exchange asynchronous factory function.
        Use it to instantiate BinanceService with proper client and socket manager.
        Example:
            binance_service = await BinanceService.init(loop)
        """
        client = await cls.create_client()
        socket_manager = BinanceSocketManager(client, loop)
        self = cls(socket_manager, client)
        return self

    @staticmethod
    async def create_client(key='', secret=''):
        return await AsyncClient.create(key, secret)
