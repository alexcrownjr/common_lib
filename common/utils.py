"""
Misc utils.
"""
import asyncio


def float_f(number, format_str="%.8f"):
    """
    Returns formatted float number.
    """
    return float(format_str % float(number))


def run_blocking_task(func):
    """
    Decorator for running blocking tasks in MarketService.

    Can be applied only to the object method (not static or class method).
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        executor = None  # use loop default executor
        task = loop.run_in_executor(executor, lambda: func(self, *args, **kwargs))
        completed, pending = await asyncio.wait([task])
        return [t.result() for t in completed][-1]
    return wrapper
