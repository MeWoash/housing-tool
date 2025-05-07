from pathlib import Path
from typing import Any
from html_parser.env import SCRAPED_DATA_DIR, POOL_SIZE
from multiprocessing import Pool
import os
from loguru import logger


async def divide_into_batches(list: list[Any], n_batches: int) -> list[list[Any]]:
    """Divides a list into n_batches of approximately equal size."""
    assert n_batches > 0 and n_batches <= len(list), "Invalid number of batches."
    batch_size = (len(list) + n_batches - 1) // n_batches
    batches = [list[i:i + batch_size] for i in range(0, len(list), batch_size)]
    logger.info(f"Divided {len(list)} elements into {len(batches)} batches with sizes {[len(batch) for batch in batches]}")
    return batches

def parse_worker(batch: list[str]) -> None:
    """Worker function to parse a batch of files."""
    for file in batch:
        file_path = Path(os.path.join(SCRAPED_DATA_DIR, file))
        # Simulate parsing the file
        # logger.info(f"Worker {os.getpid()} parsing {file_path}")
        # Add your parsing logic here

async def parse():
    files_in_dir = os.listdir(SCRAPED_DATA_DIR)
    files_to_parse = [file for file in files_in_dir if file.endswith('.html')]
    
    batches = await divide_into_batches(files_to_parse, POOL_SIZE)
    
    with Pool(POOL_SIZE) as pool:
        results = pool.map(parse_worker, batches)