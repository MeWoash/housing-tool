from typing import Any
from common.classes import OfferID, Url, DocContent
import aiofiles
from pathlib import Path
import re
from parsel import Selector
from loguru import logger

def get_offer_id_from_url(prefix: str, canonical_url: Url) -> OfferID | None:
    match = re.search(r"ID[\w\d]+", canonical_url)
    return OfferID(f"{prefix}_{match.group(0)}") if match else None


def get_offer_id_from_file(prefix: str, file_path: Path) -> OfferID | None:
    """
    Extract the offer ID from the <link rel="canonical"> tag in the HTML file.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to read file {file_path.name}: {e}")
        return None

    sel = Selector(text=content)
    canonical_url = Url(sel.xpath('//link[@rel="canonical"]/@href').get())

    if not canonical_url:
        return None

    return get_offer_id_from_url(prefix, canonical_url)

def divide_into_batches(list: list[Any], n_batches: int) -> list[list[Any]]:
    """Divides a list into n_batches of approximately equal size."""
    assert n_batches > 0 and n_batches <= len(list), "Invalid number of batches."
    batch_size = (len(list) + n_batches - 1) // n_batches
    batches = [list[i:i + batch_size] for i in range(0, len(list), batch_size)]
    logger.info(f"Divided {len(list)} elements into {len(batches)} batches with sizes {[len(batch) for batch in batches]}")
    return batches

async def write_file(
    path: Path,
    content: DocContent,
) -> None:
    async with aiofiles.open(path, "w", encoding="utf-8") as file:
        bytes_saved = await file.write(content)
        logger.info(f"Bytes saved: {bytes_saved} to {path}")


async def read_file(path: Path) -> DocContent:
    async with aiofiles.open(path, 'r', encoding="utf-8") as file:
        return DocContent(await file.read())