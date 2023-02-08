import asyncio
from functools import wraps


def typer_async(f: callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
