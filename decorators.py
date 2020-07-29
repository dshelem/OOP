"""
Decorators alter behaviour of functions.

© Denis Shelemekh, 2020

"""

from typing import Any
import time
import requests


def measure_time(func: Any) -> Any:
    """
    Measures and prints execution time for function.

    Args:
        func: Function to monitor.
    Returns:
        inner function.
    """
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time() - start
            print('%s.%s: %f' % (func.__module__, func.__name__, end - start))
    return inner


def memoize(func: any) -> Any:
    """
    Caches (string) results of function's execution.

    Args:
        func: Function to cache.
    Returns:
        inner function.
    """
    _cache = {}
    stale_time = 10  # seconds

    def wrapper(*args, **kwargs):
        name = func.__name__
        # tuple is immutable, thus hashable, thus can be a key for dictionary
        key = (name, args, frozenset(kwargs.items()))
        if key in _cache:
            value = _cache[key]
            if (time.time() - value[1]) < stale_time:
                return value[0]
        result = func(*args, **kwargs)
        _cache[key] = [result, time.time()]
        return result

    return wrapper


@measure_time
@memoize
def fetch_url(url: str) -> str:
    """
    Example of decorators' usage.
    Let's fetch the url and both measure the time of execution and cache results.

    Args:
        url: url to fetch.
    Returns:
        String - Status/encoding/length of request.
    """
    res = requests.get(url)

    ret = f"Status: {res.status_code}\n"
    ret += f"Encoding: {res.encoding}\n"
    ret += f"Content Length: {len(res.text)} bytes\n"

    return ret


def main() -> None:
    """
    Standard main function.
    """
    print(fetch_url("https://python.org"))
    print("")
    print(fetch_url("https://python.org"))
    time.sleep(11)
    print(fetch_url("https://python.org"))


if __name__ == '__main__':
    main()
