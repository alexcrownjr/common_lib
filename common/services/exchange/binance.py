from binance import AsyncClient, BinanceSocketManager

from .base import ExchangeServiceBase


class BinanceService(ExchangeServiceBase):
    """
    Binance exchange service.
    """
    socket_manager = None
    prefix = 'binance'

    def __init__(self, socket_manager=None, client=None):
        self.client = client or self.client
        self._socket_manager = socket_manager or self.socket_manager
        super(BinanceService, self).__init__()

    @classmethod
    async def init(cls, loop=None, credentials=False, **kwargs):
        """
        Initialize exchange asynchronous factory function.
        Use it to instantiate BinanceService with proper client and socket manager.
        Example:
            binance_service = await BinanceService.init(loop)
        """
        obj = await super().init()
        socket_manager = BinanceSocketManager(cls.client, loop)
        obj.socket_manager = socket_manager
        return obj

    @staticmethod
    async def create_client(key='', secret=''):
        return await AsyncClient.create(key, secret)
