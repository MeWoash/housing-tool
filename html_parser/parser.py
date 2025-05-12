from pathlib import Path
import os
from loguru import logger

from html_parser.env import BATCH_SIZE, POOL, SCRAPED_DATA_DIR
from html_parser.web_1_parser import web_1_parse_offer
from common.utils import get_offer_id_from_path, read_file
from common.fast_process import fast_multi_process
from webs.web_1_data import WEB_1_ID



async def parse_file(file_path: Path) -> None:
    """Parse a single file."""
    content = await read_file(file_path)

    offer_id = get_offer_id_from_path(file_path)
    offer_id_prefix = offer_id[:3]

    if offer_id_prefix == WEB_1_ID:
        offer = await web_1_parse_offer(content)
    else:
        logger.warning(f"Unknown offer ID prefix: {offer_id_prefix}")
        return

    if offer:
        logger.info(f"Push to DB {offer_id}: {offer}")


def parse():
    files_in_dir = os.listdir(SCRAPED_DATA_DIR)
    files = [file for file in files_in_dir if file.endswith(".html")]

    filepaths_to_parse: list[Path] = [
        Path(os.path.join(SCRAPED_DATA_DIR, file)) for file in files
    ]
    fast_multi_process(
        data=filepaths_to_parse,
        process_fnc=parse_file,
        n_processes=POOL,
        n_async_batch=BATCH_SIZE,
    )
