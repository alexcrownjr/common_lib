"""
Misc utils.
"""
import datetime
import math


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


def limit_step_size_floor(amount, step_qty):
    factor = float(1 / step_qty)
    return math.floor(factor * amount) / factor


def floor_current_time(k=4):
    now = datetime.datetime.now()
    hours = now.hour
    q, r = divmod(hours, k)
    floor_hours = q * k

    return str(now.replace(microsecond=0, second=0, minute=0, hour=floor_hours))


def str_to_datetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
