import asyncio
import json
from pathlib import Path
import os
import re
from loguru import logger
from common.classes import Url, DocContent
from parsel import Selector
import html

from html_parser.env import BATCH_SIZE, POOL, SCRAPED_DATA_DIR
from common.utils import read_file, get_offer_id_from_url
from db.models import Offer
from common.fast_process import fast_multi_process

from typing import Mapping, TypeVar

R = TypeVar("R")

def get_safe_nested(
    data: Mapping[str, object],
    keys: list[str],
    default: R
) -> R:
    """
    Traverse nested dicts/lists using keys and return final value, or default of type T.
    """
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
        
    if isinstance(value, type(default)):
        return value
    return default

def extract_json_strings(text: str) -> list[str]:
    json_strings = []
    stack = []
    start_indices = []

    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start_indices.append(i)
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    start = start_indices.pop(0)
                    candidate = text[start:i+1]
                    # Validate if it's a valid JSON object
                    try:
                        json.loads(candidate)
                        json_strings.append(candidate)
                    except json.JSONDecodeError:
                        pass  # Not a valid JSON, skip

    return json_strings


async def parse_offer(content: DocContent) -> Offer | None:
    sel = Selector(text=content)
    canonical: str | None = sel.xpath('//link[@rel="canonical"]/@href').get()
    offer_id: str | None = get_offer_id_from_url("OTO", Url(canonical))

    if not offer_id:
        logger.warning(f"Offer ID not found in {canonical}.")
        return None

    json_strings = extract_json_strings(content)

    json_data = None
    for json_string in json_strings[:20]:  # sprawdzamy tylko pierwsze 20 dla wydajności
        if '{"props":' in json_string:
            try:
                json_data = json.loads(json_string)
            except json.JSONDecodeError:
                logger.warning(f"Failed to decode JSON string: {json_string}")
            break
    if json_data is None:
        logger.warning(f"JSON data not found in {canonical}.")
        return None
    
    ad = json_data["props"]["pageProps"]["ad"]
    location = ad.get("location", {})
    address = location.get("address", {})
    coordinates = location.get("coordinates", {})
    
    characteristics_list = ad.get("characteristics", [])
    characteristics = {item["key"]: item for item in characteristics_list if "key" in item and "value" in item}

    offer = Offer(
        id=get_safe_nested(ad, ["id"], ""),
        title=get_safe_nested(ad, ["title"], ""),
        features=",".join(get_safe_nested(ad, ["features"], [])),
        description=html.unescape(get_safe_nested(ad, ["description"], "")),
        url=get_safe_nested(ad, ["url"], None),
        latitude=get_safe_nested(coordinates, ["latitude"], None),
        longitude=get_safe_nested(coordinates, ["longitude"], None),
        province=get_safe_nested(address, ["province", "name"], None),
        city=get_safe_nested(address, ["city", "name"], None),
        subregion=get_safe_nested(address, ["county", "name"], None),
        district=get_safe_nested(address, ["district", "name"], None),
        street=get_safe_nested(address, ["street", "name"], None),

        offer_type=get_safe_nested(ad, ["adCategory", "type"], None),

        price = get_safe_nested(characteristics, ["price", "value"], 0),
        size = get_safe_nested(characteristics, ["m", "value"], 0),
        rooms = get_safe_nested(characteristics, ["rooms_num", "value"], None),
        market_type=get_safe_nested(characteristics, ["market", "value"], None),
        building_type=get_safe_nested(characteristics, ["building_type", "value"], None),
        floor_number=get_safe_nested(characteristics, ["floor_no", "value"], None),
        building_floors_num=get_safe_nested(characteristics, ["building_floors_num", "value"], None),
        material=get_safe_nested(characteristics, ["building_material", "value"], None),
        window_type=get_safe_nested(characteristics, ["windows_type", "value"], None),
        heating=get_safe_nested(characteristics, ["heating", "value"], ""),
        year_built=get_safe_nested(characteristics, ["build_year", "value"], None),
        rent=get_safe_nested(characteristics, ["rent", "value"], None),
        ownership=get_safe_nested(characteristics, ["building_ownership", "value"], None),
        construction_status=get_safe_nested(characteristics, ["construction_status", "value"], None),
    )

    
    # logger.info(f"Json data: {offer}")
    return offer


async def parse_file(file_path: Path) -> None:
    """Parse a single file."""
    content = await read_file(file_path)
    _ = await parse_offer(content)
    # logger.info(f"Worker: {os.getpid()} Parsed offer: {offer}")


def parse():
    files_in_dir = os.listdir(SCRAPED_DATA_DIR)
    files = [file for file in files_in_dir if file.endswith(".html")]

    filepaths_to_parse: list[Path] = [
        Path(os.path.join(SCRAPED_DATA_DIR, file)) for file in files
    ]
    fast_multi_process(
        data=filepaths_to_parse,
        process_fnc=parse_file,
        n_processes=POOL,
        n_async_batch=BATCH_SIZE,
    )
