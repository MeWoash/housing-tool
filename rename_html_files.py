from pathlib import Path
from web_scraper.utils import get_offer_id_from_file
from loguru import logger
import os


SCRAPED_DIR = Path("scraped_data")
SOURCE = "OTO"

def file_exists_case_sensitive(path: str) -> bool:
    dir_path = os.path.dirname(path)
    target_name = os.path.basename(path)
    try:
        return target_name in os.listdir(dir_path)
    except FileNotFoundError:
        return False

def safe_rename_case_sensitive(src: str, dst: str) -> None:
    """
    Safely renames a file even if the only difference is letter casing (Windows safe).
    Copies content from src to dst and deletes src.
    """
    with open(src, "rb") as f_src:
        content = f_src.read()
    with open(dst, "wb") as f_dst:
        _ = f_dst.write(content)
    os.remove(src)

def main() -> None:
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

        new_filename = f"{offer_id}.html"
        new_path = SCRAPED_DIR / new_filename

        if file_exists_case_sensitive(str(new_path)):
            logger.warning(f"Target file already exists (case-sensitive match): {new_filename} (skipping)")
            skipped += 1
            continue

        try:
            safe_rename_case_sensitive(str(file_path), str(new_path))
            logger.info(f"Renamed {file_path.name} ➜ {new_filename}")
            renamed += 1
        except Exception as e:
            logger.error(f"Failed to rename {file_path.name}: {e}")
            skipped += 1

    logger.info(f"Renaming complete. Files renamed: {renamed}, skipped: {skipped}")

if __name__ == "__main__":
    main()
