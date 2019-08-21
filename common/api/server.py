import logging
from aiohttp.web import Application, AppRunner, TCPSite


log = logging.getLogger(__name__)


class ApiServer:
    """
    Create API server.

    Extra services example:
        redis_service = await RedisService.init(loop)
        api_server = ApiServer(routes, redis=redis_service)
        loop.create_task(api_server.start())
        loop.run_forever()
    """
    def __init__(self, routes, listen_addr=None, listen_port=None, **extra_app_params):
        self.app = Application()
        self.app.add_routes(routes)
        self._extra_params = extra_app_params
        self._listen_addr = listen_addr or '0.0.0.0'
        self._listen_port = listen_port or 3000
        self._set_extra_params()

    async def start(self):
        """
        Setup and start API application.
        """
        runner = AppRunner(self.app)
        await runner.setup()
        api_server = TCPSite(runner, host=self._listen_addr, port=self._listen_port)
        log.info("Starting API server...")
        try:
            await api_server.start()
        except BaseException:
            await runner.cleanup()

    def _set_extra_params(self):
        """
        Set api application additional services.
        """
        if not isinstance(self._extra_params, dict):
            raise BaseException("Invalid data type for extra_services")

        for name, param_value in self._extra_params.items():
            try:
                self.app[name] = param_value
            except BaseException as ex:
                log.error("Failed to initialize Redis. %s", ex)
