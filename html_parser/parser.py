import asyncio
from pathlib import Path
from typing import Any
from multiprocessing import Pool
import os
from loguru import logger
from common.classes import Url, DocContent
import re
from parsel import Selector
from loguru import logger
import json

from html_parser.env import SCRAPED_DATA_DIR, POOL_SIZE
from common.utils import read_file, get_offer_id_from_url
from db.models import Offer

def parse_offer(content: DocContent) -> Offer | None:
    
    sel = Selector(text=content)
    canonical: str | None = sel.xpath('//link[@rel="canonical"]/@href').get()
    offer_id: str | None = get_offer_id_from_url("OTO", Url(canonical))

    if not offer_id:
        logger.warning(f"Offer ID not found in {canonical}.")
        return None

    main_content = sel.xpath('//div[@data-sentry-element="MainContent"]')

    # match = re.search(r'"ad":(\{.+\})', content)
    # if match:
    #     json_string = match.group(1)
    #     json_dict  = json.loads(json_string)
    #     logger.info(json_dict)

    offer = Offer(
        id=offer_id,
        title=main_content.xpath('//h1[@data-sentry-element="Title"]/text()').get(),
        price=main_content.xpath('//strong[@data-sentry-element="Price"]/text()').get(),
        size=main_content.xpath('//div[@class="css-1ftqasz"]//text()').getall()[0],
        rooms=main_content.xpath('//div[@class="css-1ftqasz"]//text()').getall()[1],
        heating_type=main_content.xpath('//p[text()="Ogrzewanie"]/following-sibling::*[last()]//text()').get(),
        floor_number=main_content.xpath('//p[text()="Piętro"]/following-sibling::*[last()]//text()').get(),
        maintenance_cost=main_content.xpath('//p[text()="Czynsz"]/following-sibling::*[last()]//text()').get(),
        finishing_state=main_content.xpath('//p[text()="Stan wykończenia"]/following-sibling::*[last()]//text()').get(),
        market_type=main_content.xpath('//p[text()="Rynek"]/following-sibling::*[last()]//text()').get(),
        ownership_type=main_content.xpath('//p[text()="Forma własności"]/following-sibling::*[last()]//text()').get(),
        advertiser_type=main_content.xpath('//p[text()="Typ ogłoszeniodawcy"]/following-sibling::*[last()]//text()').get(),
        additional_info=", ".join(main_content.xpath('//p[text()="Informacje dodatkowe"]/following-sibling::*[last()]//span/text()').getall()),
        construction_year=main_content.xpath('//p[text()="Rok budowy"]/following-sibling::*[last()]//text()').get(),
        has_elevator=main_content.xpath('//p[text()="Winda"]/following-sibling::*[last()]//text()').get(),
        building_type_detail=main_content.xpath('//p[text()="Rodzaj zabudowy"]/following-sibling::*[last()]//text()').get(),
        material=main_content.xpath('//p[text()="Materiał budynku"]/following-sibling::*[last()]//text()').get(),
        window_type=main_content.xpath('//p[text()="Okna"]/following-sibling::*[last()]//text()').get(),
        security=main_content.xpath('//p[text()="Bezpieczeństwo"]/following-sibling::*[last()]//text()').get(),
        safety_features=", ".join(main_content.xpath('//p[text()="Zabezpieczenia"]/following-sibling::*[last()]//span/text()').getall()),
        media=", ".join(main_content.xpath('//p[text()="Media"]/following-sibling::*[last()]//span/text()').getall()),
        description=main_content.xpath('//div[@data-sentry-element="DescriptionWrapper"]').get(),
        source="otodom",
        url = sel.xpath('//link[@rel="canonical"]/@href').get()
    )
    return offer

def divide_into_batches(list: list[Any], n_batches: int) -> list[list[Any]]:
    """Divides a list into n_batches of approximately equal size."""
    assert n_batches > 0 and n_batches <= len(list), "Invalid number of batches."
    batch_size = (len(list) + n_batches - 1) // n_batches
    batches = [list[i:i + batch_size] for i in range(0, len(list), batch_size)]
    logger.info(f"Divided {len(list)} elements into {len(batches)} batches with sizes {[len(batch) for batch in batches]}")
    return batches

async def parse_file(file_path: Path) -> None:
    """Parse a single file."""
    content = await read_file(file_path)
    offer = parse_offer(content)
    # logger.info(f"Worker: {os.getpid()} Parsed offer: {offer}")

async def parse_worker(batch: list[str]) -> None:
    """Worker function to parse a batch of files."""
    for file in batch:
        file_path = Path(os.path.join(SCRAPED_DATA_DIR, file))
        await parse_file(file_path)

def run_parse_worker_async(batch: list[str]) -> None:
    return asyncio.run(parse_worker(batch))

def parse():
    files_in_dir = os.listdir(SCRAPED_DATA_DIR)
    files_to_parse = [file for file in files_in_dir if file.endswith('.html')][:1000]
    
    if POOL_SIZE <= 1:
        logger.info("Running in async mode")
        results = run_parse_worker_async(files_to_parse)
    else:
        logger.info(f"Running in multiprocessing mode with {POOL_SIZE} workers")
        batches = divide_into_batches(files_to_parse, POOL_SIZE)
        with Pool(POOL_SIZE) as pool:
            results = pool.map(run_parse_worker_async, batches)