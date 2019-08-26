"""
Misc utils.
"""
import asyncio
import math


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
