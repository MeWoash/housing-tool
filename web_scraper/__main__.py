import asyncio
from web_scraper.scraper import scrape
# from web_scraper import web_scraper

async def web_scraper_main():
    await scrape()

asyncio.run(web_scraper_main())