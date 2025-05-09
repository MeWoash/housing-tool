from web_scraper.web_1_scraper import get_web_1_scraper

async def run_scrapers() -> None:
    web_1_scraper_instance = await get_web_1_scraper()
    await web_1_scraper_instance.run()
    
