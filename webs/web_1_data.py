from pathlib import Path
import re
from common.classes import OfferId, SubUrl, Url
from webs.env import SCRAPED_DATA_DIR

WEB_1_ID = ""
WEB_1_BASE_URL = ""
WEB_1_PAGINATION_URL = "" 
WEB_1_PAGINATION_URL_PREFIX_FILTER = ""
WEB_1_ID_GEN_REGEX = r""

WEB_1_DATA_DIR = Path(SCRAPED_DATA_DIR, WEB_1_ID)

def web_1_process_urls(urls: list[Url | SubUrl]) -> list[Url]:
    """
    Filter URLs to include only those that match the desired pattern.
    """
    filtered_urls = [
        Url(WEB_1_BASE_URL + url) for url in urls if WEB_1_PAGINATION_URL_PREFIX_FILTER in url
    ]
    return filtered_urls


def web_1_get_offer_id_from_url(canonical_url: Url | SubUrl) -> OfferId | None:
    match = re.search(WEB_1_ID_GEN_REGEX, canonical_url)
    return OfferId(f"{WEB_1_ID}_{match.group(1)}") if match else None