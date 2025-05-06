from loguru import logger
from web_scraper.env import SCRAPED_DATA_DIR, BASE_URL
from web_scraper.headers import get_headers
import asyncio
import httpx
from parsel import Selector
from pathlib import Path
import aiofiles
import random
from web_scraper.utils import DocContent, Url, get_offer_id_from_url

HTTPX_CLIENT = httpx.AsyncClient()


async def create_page_url(page_number: int = 1) -> Url:
    return Url(
        BASE_URL
        + f"/pl/wyniki/sprzedaz/mieszkanie/zachodniopomorskie/szczecin/szczecin/szczecin?limit=72&ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC&viewType=listing&page={page_number}"
    )


async def download_page(url: Url) -> DocContent:
    headers = get_headers()
    response = await HTTPX_CLIENT.get(url, headers=headers)
    _ = response.raise_for_status()

    return DocContent(response.text)


async def load_page(path: Path) -> DocContent:
    async with aiofiles.open(path, "r", encoding="utf-8") as file:
        content = await file.read()
    return DocContent(content)


def get_page_path(url: Url) -> Path:
    path = SCRAPED_DATA_DIR / f"{get_offer_id_from_url('OTO', url)}.html"
    return path


async def save_page(
    path: Path,
    content: DocContent,
) -> None:
    async with aiofiles.open(path, "w", encoding="utf-8") as file:
        bytes_saved = await file.write(content)
        logger.info(f"Bytes saved: {bytes_saved}")


async def get_offers_from_page(page_number: int) -> list[Url]:
    query_url = await create_page_url(page_number)

    content = await download_page(query_url)

    selector = Selector(content)
    a_elements = selector.xpath("//a/@href").getall()
    offers: list[Url] = [
        Url(BASE_URL + offer) for offer in a_elements if offer.startswith("/pl/oferta")
    ]

    logger.info(f"Scraped {len(offers)} offers from page {page_number}.")
    return offers


async def scrape() -> None:
    offer_urls_seen: set[Url] = set()
    offer_urls_to_download: list[Url] = []

    pageCounter = 1
    while True:
        try:
            offer_urls_to_download += await get_offers_from_page(pageCounter)
        except Exception:
            logger.exception(f"Failed to download page {pageCounter}")
            continue

        sleep = random.uniform(8, 12)
        logger.info(f"Delay after pagination for {sleep} seconds...")
        await asyncio.sleep(sleep)

        while offer_urls_to_download:
            url = offer_urls_to_download.pop(0)

            if url in offer_urls_seen:
                continue
            offer_urls_seen.add(url)

            logger.info(
                f"Page: {pageCounter}\t to download: {len(offer_urls_to_download)}\tseen: {len(offer_urls_seen)}"
            )

            path = get_page_path(url)

            if path.exists():
                continue
            else:
                logger.info(f"Downloading {url}...")

                try:
                    doc_content = await download_page(url)
                    logger.info(f"Downloaded {url} to {path}.")
                except Exception:
                    logger.exception(f"Failed to download {url}")
                    continue
                await save_page(path, doc_content)
                sleep = random.uniform(8, 12)
                logger.info(f"Delay after offer for {sleep} seconds...")
                await asyncio.sleep(sleep)

        pageCounter += 1
