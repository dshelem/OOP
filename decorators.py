import time
import requests


def measure_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            ex_time = time.time() - start_time
            print(f"Execution time: {ex_time: .2f} seconds")
    return inner


def memoize(func):
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
def fetch_url(url):
    res = requests.get(url)

    ret = f"Status: {res.status_code}\n"
    ret += f"Encoding: {res.encoding}\n"
    ret += f"Content Length: {len(res.text)} bytes\n"

    return ret

print(fetch_url("https://python.org"))
print("")
print(fetch_url("https://python.org"))
time.sleep(11)
print(fetch_url("https://python.org"))
