from common.classes import OfferId, SubUrl, Url
from web_scraper.common_scraper import BaseScrapper
from webs.web_1_data import WEB_1_BASE_URL, WEB_1_DATA_DIR, WEB_1_ID, WEB_1_PAGINATION_URL, web_1_process_urls, web_1_get_offer_id_from_url
import asyncio

class Web1Scraper(BaseScrapper):

    def __init__(self) -> None:
        super().__init__(
            web_id=WEB_1_ID,
            web_base_url=WEB_1_BASE_URL,
            web_pag_url=WEB_1_PAGINATION_URL,
            web_scraped_data_Dir=WEB_1_DATA_DIR,
            request_delay_range=(8, 12),
        )

    async def urls_process_function(self, urls: list[Url | SubUrl]) -> list[Url]:
        return web_1_process_urls(urls)

    async def id_generator_function(self, url: Url | SubUrl) -> OfferId | None:
        return web_1_get_offer_id_from_url(url)


async def run_scrapers() -> None:
    web_1_scraper_instance = Web1Scraper()

    tasks = [
        web_1_scraper_instance.run()
    ]

    _ = await asyncio.gather(*tasks)
    
