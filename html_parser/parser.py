from pathlib import Path
import os
from loguru import logger
from common.classes import Url, DocContent
from parsel import Selector

from html_parser.env import BATCH_SIZE, POOL, SCRAPED_DATA_DIR
from common.utils import read_file, get_offer_id_from_url
from db.models import Offer
from common.fast_process import fast_multi_process


async def parse_offer(content: DocContent) -> Offer | None:
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
        heating_type=main_content.xpath(
            '//p[text()="Ogrzewanie"]/following-sibling::*[last()]//text()'
        ).get(),
        floor_number=main_content.xpath(
            '//p[text()="Piętro"]/following-sibling::*[last()]//text()'
        ).get(),
        maintenance_cost=main_content.xpath(
            '//p[text()="Czynsz"]/following-sibling::*[last()]//text()'
        ).get(),
        finishing_state=main_content.xpath(
            '//p[text()="Stan wykończenia"]/following-sibling::*[last()]//text()'
        ).get(),
        market_type=main_content.xpath(
            '//p[text()="Rynek"]/following-sibling::*[last()]//text()'
        ).get(),
        ownership_type=main_content.xpath(
            '//p[text()="Forma własności"]/following-sibling::*[last()]//text()'
        ).get(),
        advertiser_type=main_content.xpath(
            '//p[text()="Typ ogłoszeniodawcy"]/following-sibling::*[last()]//text()'
        ).get(),
        additional_info=", ".join(
            main_content.xpath(
                '//p[text()="Informacje dodatkowe"]/following-sibling::*[last()]//span/text()'
            ).getall()
        ),
        construction_year=main_content.xpath(
            '//p[text()="Rok budowy"]/following-sibling::*[last()]//text()'
        ).get(),
        has_elevator=main_content.xpath(
            '//p[text()="Winda"]/following-sibling::*[last()]//text()'
        ).get(),
        building_type_detail=main_content.xpath(
            '//p[text()="Rodzaj zabudowy"]/following-sibling::*[last()]//text()'
        ).get(),
        material=main_content.xpath(
            '//p[text()="Materiał budynku"]/following-sibling::*[last()]//text()'
        ).get(),
        window_type=main_content.xpath(
            '//p[text()="Okna"]/following-sibling::*[last()]//text()'
        ).get(),
        security=main_content.xpath(
            '//p[text()="Bezpieczeństwo"]/following-sibling::*[last()]//text()'
        ).get(),
        safety_features=", ".join(
            main_content.xpath(
                '//p[text()="Zabezpieczenia"]/following-sibling::*[last()]//span/text()'
            ).getall()
        ),
        media=", ".join(
            main_content.xpath(
                '//p[text()="Media"]/following-sibling::*[last()]//span/text()'
            ).getall()
        ),
        description=main_content.xpath(
            '//div[@data-sentry-element="DescriptionWrapper"]'
        ).get(),
        source="otodom",
        url=sel.xpath('//link[@rel="canonical"]/@href').get(),
    )
    return offer


async def parse_file(file_path: Path) -> None:
    """Parse a single file."""
    content = await read_file(file_path)
    _ = await parse_offer(content)
    # logger.info(f"Worker: {os.getpid()} Parsed offer: {offer}")


def parse():
    files_in_dir = os.listdir(SCRAPED_DATA_DIR)
    files = [file for file in files_in_dir if file.endswith(".html")][:1000]

    filepaths_to_parse: list[Path] = [
        Path(os.path.join(SCRAPED_DATA_DIR, file)) for file in files
    ]
    fast_multi_process(
        data=filepaths_to_parse,
        process_fnc=parse_file,
        n_processes=POOL,
        n_async_batch=BATCH_SIZE,
    )
