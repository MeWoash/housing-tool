import asyncio
from html_parser.parser import parse
from common.time_manager import timeit
# from web_scraper import web_scraper

@timeit
async def html_parser_main():
    await parse()

asyncio.run(html_parser_main())