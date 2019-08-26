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
    return str(int(f)) if int(n) == 0 else f
