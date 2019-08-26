"""
Market exchange services.
"""
from binance import AsyncClient, BinanceSocketManager

from common.utils import float_f


class ExchangeServiceBase:
    """
    Exchange base class.
    """
    client = None

    def __init__(self):
        if self.client is None:
            raise Exception("Improperly configured service client")


class BinanceService(ExchangeServiceBase):
    """
    Binance exchange service.
    """
    socket_manager = None

    def __init__(self, client, socket_manager):
        self.client = client
        self._socket_manager = socket_manager
        super(BinanceService, self).__init__()

    @classmethod
    async def init(cls, loop):
        """
        Initialize exchange asynchronous factory function.
        Use it to instantiate BinanceService with proper client and socket manager.
        Example:
            binance_service = await BinanceService.init(loop)
        """
        client = await AsyncClient.create()
        socket_manager = BinanceSocketManager(cls.client, loop)
        return cls(client, socket_manager)
