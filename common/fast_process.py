import asyncio
import inspect
from pathlib import Path
from multiprocessing import Pool
import os
from typing import Any, Callable, Iterable
from loguru import logger
from common.utils import divide_into_batches, batch_list

async def __async_worker(args: tuple[list[Any], Callable[..., Any], int]) -> None:
    """Async worker function to parse a batch of files."""
    data, process_fnc, n_batches = args
    for async_batch in batch_list(data, n_batches):
        tasks = [asyncio.create_task(process_fnc(batch_element)) for batch_element in async_batch]
        results = await asyncio.gather(*tasks) # type: ignore
        
def __sync_worker(args: tuple[list[Any], Callable[..., Any], int]) -> None:
    """Sync worker function to parse a batch of files."""
    data, process_fnc, n_batches = args # type: ignore
    for element in data:
        process_fnc(element)

def __run_worker(args: tuple[list[Any], Callable[..., Any], int]) -> None:
    """Run the worker function based on the type of process function."""
    if inspect.iscoroutinefunction(args[1]):
        logger.info(f"Running in async mode with {args[2]} batches")
        return asyncio.run(__async_worker(args))
    else:
        logger.info(f"Running in sync mode")
        return __sync_worker(args)

def fast_multi_process(
    data: list[Any],
    process_fnc: Callable[..., Any],
    n_processes: int = 1,
    n_async_batch:int = 1
    ) -> None:
    """
    Function dispatches work over a pool of processes and handles asynchronous batches defined by n_async_batch.
    This design improves throughput by leveraging parallel execution and asynchronous batch processing.
    """
    
    if n_processes <= 1:
        logger.info(f"Running in single process")
        results = __run_worker((data, process_fnc, n_async_batch)) # type: ignore
    else:
        logger.info(f"Running in multiprocessing({n_processes} workers)")
        batches = divide_into_batches(data, n_processes)
        args = zip(batches, [process_fnc]*len(batches), [n_async_batch]*len(batches))
        with Pool(n_processes) as pool:
            results = pool.map(__run_worker, args) # type: ignore