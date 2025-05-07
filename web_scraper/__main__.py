import asyncio
from web_scraper.scraper import scrape

async def web_scraper_main():
    await scrape()

asyncio.run(web_scraper_main())