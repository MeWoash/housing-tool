import time
import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def timeit(func: F) -> F:
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            print(f"[{func.__name__}] took {end - start:.6f} seconds (async).")
            return result

        return cast(F, async_wrapper)
    else:

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"[{func.__name__}] took {end - start:.6f} seconds.")
            return result

        return cast(F, sync_wrapper)
