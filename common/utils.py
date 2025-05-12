from common.classes import OfferId, DocContent
import aiofiles
from pathlib import Path
from loguru import logger

def get_offer_id_from_path(file_path: Path) -> OfferId:
    """
    Extract the offer ID from the file name.
    """
    return OfferId(file_path.stem)

async def write_file(
    path: Path,
    content: DocContent,
) -> None:
    bytes_saved = 0
    try:
        async with aiofiles.open(path, "w", encoding="utf-8") as file:
            bytes_saved = await file.write(content)
        logger.info(f"Saved {bytes_saved} bytes to {path}.")
    except Exception as e:
        logger.info(f"Failed to write file {path}: {e}")


async def read_file(path: Path) -> DocContent:
    async with aiofiles.open(path, "r", encoding="utf-8") as file:
        return DocContent(await file.read())
