"""
Misc utils.
"""
import asyncio
import datetime
import math
import time


def raise_KeyError(msg=''): raise KeyError(msg)


def time_spent(logger):
    """
    Measure time spent on `func` coroutine execution.
    """
    def decorator_wrapper(func):
        async def process(func, *args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        async def wrapper(*args, **kwargs):
            s = time.perf_counter()
            result = await process(func, *args, **kwargs)
            elapsed = time.perf_counter() - s
            logger.info(f"{func.__name__} time = {elapsed}")
            return result
        return wrapper

    return decorator_wrapper    

def float_to_str(f):
    float_string = repr(f)
    if 'e' in float_string:  # detect scientific notation
        digits, exp = float_string.split('e')
        digits = digits.replace('.', '').replace('-', '')
        exp = int(exp)
        zero_padding = '0' * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
        sign = '-' if f < 0 else ''
        if exp > 0:
            float_string = '{}{}{}.0'.format(sign, digits, zero_padding)
        else:
            float_string = '{}0.{}{}'.format(sign, zero_padding, digits)
    return float_string


def utc_now():
    return datetime.datetime.utcnow().replace(microsecond=0)


def is_crossing_actual(crossing_created):
    time_now = utc_now()
    crossing_created = str_to_datetime(crossing_created)
    delta = (time_now - crossing_created)

    return delta.seconds < 70


def float_f(number, format_str="%.8f"):
    """
    Returns formatted float number.
    """
    return float(format_str % float(number))


def float_precision(f, n):
    n = int(math.log10(1 / float(n)))
    f = math.floor(float(f) * 10 ** n) / 10 ** n
    f = "{:0.0{}f}".format(float(f), n)
    return float(str(int(f)) if int(n) == 0 else f)

def qty_precision(quantity, stepSize):
    precision = int(round(-math.log(stepSize, 10), 0))
    return round(quantity, precision)


def limit_step_size_floor(amount, step_qty):
    factor = float(1 / step_qty)
    return math.floor(factor * amount) / factor


def floor_time(time, k=4):
    hours = time.hour
    q, r = divmod(hours, k)
    floor_hours = q * k
    return str(time.replace(microsecond=0, second=0, minute=0, hour=floor_hours))


def floor_datetime(date_time_str, k=4):
    time = str_to_datetime(date_time_str)
    return floor_time(time)


def floor_current_time(k=4):
    now = datetime.datetime.now()
    return floor_time(now)


def str_to_datetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
