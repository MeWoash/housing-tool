from asyncio import taskgroups
from web_scraper.BaseScraper import BaseScrapper
from webs.web_1_data import WEB_1_BASE_URL, WEB_1_DATA_DIR, WEB_1_ID, WEB_1_PAGINATION_URL, web_1_filter_urls, web_1_get_offer_id_from_url
import asyncio

async def get_web_1_scraper() -> BaseScrapper:
    """
    Create a new instance of the web 1 scraper.
    """
    return BaseScrapper(
        web_id=WEB_1_ID,
        web_base_url=WEB_1_BASE_URL,
        web_pag_url=WEB_1_PAGINATION_URL,
        urls_filter_function=web_1_filter_urls,
        id_generator_function=web_1_get_offer_id_from_url,
        web_scraped_data_Dir = WEB_1_DATA_DIR,
        request_delay_range=(8, 12),
    )


async def run_scrapers() -> None:
    web_1_scraper_instance = await get_web_1_scraper()

    tasks = [
        web_1_scraper_instance.run()
    ]

    _ = await asyncio.gather(*tasks)
    
