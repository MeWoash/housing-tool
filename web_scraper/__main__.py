import asyncio
from web_scraper.scraper import run_scrapers

async def web_scraper_main():
    await run_scrapers()

asyncio.run(web_scraper_main())