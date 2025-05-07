import os
import re

from parsel import Selector
from loguru import logger
import json
from common.utils import get_offer_id_from_url
from common.classes import Url
from db.models import Offer

SCRAPED_DIR: str = "scraped_data"
SOURCE: str = "otodom"




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
