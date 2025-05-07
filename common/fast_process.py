import asyncio
import inspect
from multiprocessing import Pool
from typing import Any, Callable, Awaitable, TypeAlias
from loguru import logger
from common.utils import divide_into_batches, batch_list
import os

Pfnc: TypeAlias = Callable[..., Any]

async def async_process_data(data: list[Any], process_fnc: Pfnc, n_batches: int) -> None:
    """Async worker function to parse a batch of files."""
    for async_batch in batch_list(data, n_batches):
        tasks = [asyncio.create_task(process_fnc(batch_element)) for batch_element in async_batch]
        results = await asyncio.gather(*tasks)  # type: ignore

def process_data(data: list[Any], process_fnc: Pfnc, n_batches: int) -> None:
    """Sync worker function to parse a batch of files."""
    for element in data:
        process_fnc(element)

def __run_worker(data: list[Any], process_fnc: Pfnc, n_batches: int) -> None:
    """Run the worker function based on the type of process function."""
    if inspect.iscoroutinefunction(process_fnc):
        logger.info(f"PID: {os.getpid()} running in async mode with {n_batches} batches")
        return asyncio.run(async_process_data(data, process_fnc, n_batches))
    else:
        logger.info(f"PID: {os.getpid()} running in sync mode")
        return process_data(data, process_fnc, n_batches)

def fast_multi_process(
    data: list[Any],
    process_fnc: Pfnc,
    n_processes: int = 1,
    n_async_batch: int = 1
) -> None:
    """
    Function dispatches work over a pool of processes and handles asynchronous batches.
    This design improves throughput by leveraging parallel execution and asynchronous batch processing.
    """
    
    if n_processes <= 1:
        logger.info("Running in single process")
        __run_worker(data, process_fnc, n_async_batch)  # CHANGED
    else:
        logger.info(f"Running in multiprocessing ({n_processes} workers)")
        batches = divide_into_batches(data, n_processes)
        args = list(zip(batches, [process_fnc] * len(batches), [n_async_batch] * len(batches)))
        with Pool(n_processes) as pool:
            pool.starmap(__run_worker, args) # type: ignore