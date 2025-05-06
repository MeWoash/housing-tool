import os
import re

from parsel import Selector
from loguru import logger
import json

from db.models import Offer

SCRAPED_DIR: str = "scraped_data"
SOURCE: str = "otodom"

def get_first(sel: Selector, xpath: str) -> str | None:
    result = sel.xpath(xpath).get()
    return result.strip() if result else None

def extract_offer_id(canonical_url: str | None) -> str | None:
    if not canonical_url:
        return None
    match = re.search(r'ID[\w\d]+', canonical_url)
    return f"{SOURCE}_{match.group(0)}" if match else None

def parse_offer(file_path: str) -> Offer | None:
    with open(file_path, "r", encoding="utf-8") as f:
        content: str = f.read()

    sel = Selector(text=content)

    canonical: str | None = get_first(sel, '//link[@rel="canonical"]/@href')
    offer_id: str | None = extract_offer_id(canonical)

    if not offer_id:
        print(f"Brak ID w {file_path}")
        return None

    main_content = sel.xpath('//div[@data-sentry-element="MainContent"]')

    match = re.search(r'"ad":(\{.+\})', content)
    if match:
        json_string = match.group(1)
        json_dict  = json.loads(json_string)
        logger.info(json_dict)

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


def main() -> None:
    # session: Session = get_session()
    inserted: int = 0

    for filename in os.listdir(SCRAPED_DIR):
        if not filename.endswith(".html"):
            continue

        filepath: str = os.path.join(SCRAPED_DIR, filename)
        offer: Offer | None = parse_offer(filepath)
        offer = offer
        logger.info(f"Offer {offer}")
        # if not offer:
        #     continue

        # if session.get(Offer, offer.id):
        #     skipped += 1
        #     continue

        # session.add(offer)
        inserted += 1

    # session.commit()

if __name__ == "__main__":
    main()
