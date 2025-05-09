from pathlib import Path
from webs.env import SCRAPED_DATA_DIR


WEB_1_ID = "OTO"
WEB_1_BASE_URL = "https://www.otodom.pl"
WEB_1_PAGINATION_URL = "/pl/wyniki/sprzedaz/mieszkanie/zachodniopomorskie/szczecin/szczecin/szczecin?limit=72&ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC&viewType=listing&page={page_number}" 
WEB_1_PAGINATION_URL_PREFIX_FILTER = "/pl/oferta"
WEB_1_DATA_DIR = Path(SCRAPED_DATA_DIR, WEB_1_ID)
WEB_1_ID_GEN_REGEX = r"ID([\w\d]+)"