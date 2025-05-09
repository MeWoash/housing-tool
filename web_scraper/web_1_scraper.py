import re

from common.classes import Url
from web_scraper.BaseScraper import BaseScrapper

from webs.web_1_data import WEB_1_BASE_URL, WEB_1_DATA_DIR, WEB_1_ID, WEB_1_ID_GEN_REGEX, WEB_1_PAGINATION_URL, WEB_1_PAGINATION_URL_PREFIX_FILTER


def web_1_filter_urls(urls: list[str]) -> list[Url]:
    """
    Filter URLs to include only those that match the desired pattern.
    """
    filtered_urls = [
        Url(WEB_1_BASE_URL + url) for url in urls if WEB_1_PAGINATION_URL_PREFIX_FILTER in url
    ]
    return filtered_urls


def get_offer_id_from_url(canonical_url: Url) -> str | None:
    match = re.search(WEB_1_ID_GEN_REGEX, canonical_url)
    return f"{WEB_1_ID}_{match.group(1)}" if match else None


async def get_web_1_scraper() -> BaseScrapper:
    """
    Create a new instance of the web 1 scraper.
    """
    return BaseScrapper(
        web_id=WEB_1_ID,
        web_base_url=WEB_1_BASE_URL,
        web_pag_url=WEB_1_PAGINATION_URL,
        urls_filter_function=web_1_filter_urls,
        id_generator_function=get_offer_id_from_url,
        web_scraped_data_Dir = WEB_1_DATA_DIR,
        request_delay_range=(8, 12),
    )