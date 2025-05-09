from pathlib import Path
import re
from common.classes import Url
from webs.env import SCRAPED_DATA_DIR

WEB_1_ID = "OTO"
WEB_1_BASE_URL = "https://www.otodom.pl"
WEB_1_PAGINATION_URL = "/pl/wyniki/sprzedaz/mieszkanie/zachodniopomorskie/szczecin/szczecin/szczecin?limit=72&ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC&viewType=listing&page={page_number}" 
WEB_1_PAGINATION_URL_PREFIX_FILTER = "/pl/oferta"
WEB_1_DATA_DIR = Path(SCRAPED_DATA_DIR, WEB_1_ID)
WEB_1_ID_GEN_REGEX = r"ID([\w\d]+)"

def web_1_filter_urls(urls: list[str]) -> list[Url]:
    """
    Filter URLs to include only those that match the desired pattern.
    """
    filtered_urls = [
        Url(WEB_1_BASE_URL + url) for url in urls if WEB_1_PAGINATION_URL_PREFIX_FILTER in url
    ]
    return filtered_urls


def web_1_get_offer_id_from_url(canonical_url: Url) -> str | None:
    match = re.search(WEB_1_ID_GEN_REGEX, canonical_url)
    return f"{WEB_1_ID}_{match.group(1)}" if match else None