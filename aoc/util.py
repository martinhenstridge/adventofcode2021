import operator
import functools
from os.path import abspath, dirname, join


_ROOT = dirname(dirname(abspath(__file__)))


def get_input_lines(name):
    path = join(_ROOT, "inputs", name)
    with open(path) as f:
        return f.read().splitlines()


def product(numbers):
    return functools.reduce(operator.mul, numbers, 1)


def memoize(fn):
    cache = {}
    @functools.wraps(fn)
    def wrapped(key, *args, **kwargs):
        if key not in cache:
            cache[key] = fn(key, *args, **kwargs)
        return cache[key]
    return wrapped
