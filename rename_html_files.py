import asyncio
import os
from pathlib import Path
from loguru import logger
from common.classes import OfferID
from common.utils import get_offer_id_from_file
import aiofiles

SCRAPED_DIR = Path("scraped_data")
SOURCE = "OTO"


def file_exists_case_sensitive(path: str) -> bool:
    dir_path = os.path.dirname(path)
    target_name = os.path.basename(path)
    try:
        return target_name in os.listdir(dir_path)
    except FileNotFoundError:
        return False


async def safe_rename_case_sensitive(src: Path, dst: Path) -> None:
    """
    Safely renames a file even if the only difference is letter casing (Windows safe).
    Copies content from src to dst and deletes src.
    """
    async with aiofiles.open(src, "rb") as f_src:
        content = await f_src.read()
    async with aiofiles.open(dst, "wb") as f_dst:
        bytes = await f_dst.write(content)
        logger.debug(f"Bytes copied: {bytes}")
    os.remove(src)


def get_file_name(offer_id: OfferID) -> str:
    return f"{offer_id}.html"


async def main() -> None:
    renamed = 0
    skipped = 0

    logger.info("Starting HTML file renaming process...")

    for file_path in SCRAPED_DIR.iterdir():
        if not file_path.name.endswith(".html") or not file_path.is_file():
            continue

        offer_id = get_offer_id_from_file("OTO", file_path)

        if not offer_id:
            logger.warning(f"Missing offer ID in file: {file_path.name}")
            skipped += 1
            continue

        new_filename = get_file_name(offer_id)
        new_path = SCRAPED_DIR / new_filename

        if file_exists_case_sensitive(str(new_path)):
            logger.warning(
                f"Target file already exists (case-sensitive match): {new_filename} (skipping)"
            )
            skipped += 1
            continue

        try:
            await safe_rename_case_sensitive(file_path, new_path)
            logger.info(f"Renamed {file_path.name} ➜ {new_filename}")
            renamed += 1
        except Exception as e:
            logger.error(f"Failed to rename {file_path.name}: {e}")
            skipped += 1

    logger.success(f"Renaming complete. Files renamed: {renamed}, skipped: {skipped}")


if __name__ == "__main__":
    asyncio.run(main())
