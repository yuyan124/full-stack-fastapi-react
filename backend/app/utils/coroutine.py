from functools import wraps
import asyncio


def coro_wrap(f:callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
