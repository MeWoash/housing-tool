from loguru import logger
from pathlib import Path
from parsel import Selector
import re
import hashlib


class DocContent(str):
    pass


class Url(str):
    def hash(self) -> str:
        return hashlib.md5(self.encode()).hexdigest()[:8].lower()


class OfferID(str):
    pass


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
