import asyncio
from collections.abc import Coroutine
from dataclasses import dataclass
from multiprocessing import Pool
from typing import Callable, Generic, TypeVar

import more_itertools as mit
from loguru import logger

_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(eq=True, frozen=True)
class ProcessArgs(Generic[_T, _R]):
    data: list[_T]
    process_fnc: Callable[[_T], Coroutine[None, _T, _R]]
    n_async_batch: int


async def async_process_data(
    args: ProcessArgs[_T, _R],
) -> None:
    """Async worker function to parse a batch of files."""
    for async_batch in mit.chunked(args.data, args.n_async_batch):
        tasks: list[asyncio.Task[_R]] = [
            asyncio.create_task(args.process_fnc(batch_element))
            for batch_element in async_batch
        ]
        _ = await asyncio.gather(*tasks)


def __run_worker(args: ProcessArgs[_T, _R]) -> None:
    """Run the worker function based on the type of process function."""
    asyncio.run(async_process_data(args))


def fast_multi_process(
    data: list[_T],
    process_fnc: Callable[[_T], Coroutine[None, _T, _R]],
    n_processes: int = 1,
    n_async_batch: int = 1,
) -> None:
    """
    Function dispatches work over a pool of processes and handles asynchronous batches.
    This design improves throughput by leveraging parallel execution and asynchronous batch processing.
    """

    match n_processes:
        case 0:
            raise ValueError("Number of processes must be greater than 0")
        case 1:
            logger.info("Running in single process")
            __run_worker(ProcessArgs(data, process_fnc, n_async_batch))
        case _:
            logger.info(f"Running in multiprocessing ({n_processes} workers)")
            batches = [list(batch) for batch in mit.distribute(n_processes, data)]
            args = [ProcessArgs(batch, process_fnc, n_async_batch) for batch in batches]

            with Pool(n_processes) as pool:
                _ = pool.map(__run_worker, args)
