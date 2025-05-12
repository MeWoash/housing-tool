from abc import abstractmethod
from pathlib import Path
import random
from typing import Callable, Tuple, cast

import aiofiles
import httpx
from parsel import Selector
from common.classes import DocContent, OfferId, SubUrl, Url
from common.utils import write_file
from web_scraper.headers import get_headers
from loguru import logger
import asyncio
import time

UrlProcessFunction = Callable[[list[Url | SubUrl]], list[Url]]
IdGeneratorFunction = Callable[[Url | SubUrl], OfferId | None]

class BaseScrapper:
    """
    Base class for web scrapers.
    """
    
    def __init__(
        self,
        web_id: str,
        web_base_url: str,
        web_pag_url: str,
        web_scraped_data_Dir: Path,
        request_delay_range: Tuple[int, int] = (8,12),
        ) -> None:

        self.web_base_url = web_base_url
        self.web_pagination_url = web_pag_url
        self.web_id = web_id
        self.last_request_timestamp: float = 0
        self.request_delay_range = request_delay_range

        # prepare the directory for scraped data
        web_scraped_data_Dir.mkdir(parents=True, exist_ok=True)
        self.scraped_data_dir: Path = web_scraped_data_Dir

        self.HTTPX_CLIENT = httpx.AsyncClient()
    
    @abstractmethod
    async def urls_process_function(self, urls: list[Url | SubUrl]) -> list[Url]:
        ...

    @abstractmethod
    async def id_generator_function(self, url: Url | SubUrl) -> OfferId | None:
        ...
    
    async def generate_pagination_url(self, page_number: int) -> Url:
        return Url(self.web_base_url + self.web_pagination_url.format(page_number=page_number))

    async def scrape_pagination(self, content: DocContent) -> list[Url] | None:

        selector = Selector(content)
        a_elements = cast(list[Url | SubUrl], selector.xpath("//a/@href").getall())

        offers: list[Url] = await self.urls_process_function(a_elements)
        logger.info(f"After filtering {len(offers)} / {len(a_elements)} offers on page.")
        return offers
    
    async def load_page(self, path: Path) -> DocContent:
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            content = await file.read()
        return DocContent(content)
    
    async def download_page(self, url: Url) -> DocContent | None:
        # throttle requests: ensure at least N seconds between calls
        now = time.time()
        elapsed = now - self.last_request_timestamp
        interval = random.uniform(*self.request_delay_range)
        if elapsed < interval:
            to_wait = interval - elapsed
            logger.info(f"Need to wait for {to_wait:2.2f}/{interval:2.2f} seconds before next request...")
            await asyncio.sleep(to_wait)      

        headers = get_headers()
        try:
            logger.info(f"Downloading {url}...")
            response = await self.HTTPX_CLIENT.get(url, headers=headers)
            self.last_request_timestamp = time.time()
            _ = response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
            
        return DocContent(response.text)
    
    async def generate_page_path(self, url: Url | SubUrl) -> Path | None:
        """
        Generate a path for the given URL.
        """
        id = await self.id_generator_function(url)
        if id is None:
            logger.error(f"Failed to generate ID for URL: {url}")
            return None
        return self.scraped_data_dir / f"{id}.html"
    
    async def run(self):
        offer_urls_seen: set[Url] = set()
        pageCounter = 1

        while True:
            pagin_url = await self.generate_pagination_url(pageCounter)
            pag_content = await self.download_page(pagin_url)
            if pag_content is None:
                continue
            offer_urls_to_download = await self.scrape_pagination(pag_content)
            if offer_urls_to_download is None:
                continue

            while offer_urls_to_download:
                url = offer_urls_to_download.pop(0)

                if url in offer_urls_seen:
                    continue
                offer_urls_seen.add(url)

                logger.info(f"Page: {pageCounter}\t to download: {len(offer_urls_to_download)}\tseen: {len(offer_urls_seen)}")

                path = await self.generate_page_path(url)
                if path is None:
                    logger.error(f"Failed to generate path for URL: {url}")
                    continue

                if path.exists():
                    continue

                doc_content = await self.download_page(url)
                if doc_content is None:
                    continue

                await write_file(path, doc_content)
    
