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

from typing import Dict, List, Mapping, Optional, TypeVar, TypedDict, Union, cast

import msgspec

JsonType = Union[None, int, str, bool, List['JsonType'], Dict[str, 'JsonType']]

class Coordinates(msgspec.Struct):
    latitude: Optional[float]
    longitude: Optional[float]


class Address(msgspec.Struct):
    province: Optional[str]
    city: Optional[str]
    subregion: Optional[str]
    district: Optional[str]
    street: Optional[str]


class Characteristics(msgspec.Struct):
    price: Optional[int] = 0
    size: Optional[int] = 0
    rooms: Optional[int] = None
    market_type: Optional[str] = None
    building_type: Optional[str] = None
    floor_number: Optional[int] = None
    building_floors_num: Optional[int] = None
    material: Optional[str] = None
    window_type: Optional[str] = None
    heating: Optional[str] = ""
    year_built: Optional[int] = None
    rent: Optional[int] = None
    ownership: Optional[str] = None
    construction_status: Optional[str] = None


class Ad(msgspec.Struct):
    id: int
    title: str
    features: str
    description: str
    url: Optional[str]

    coordinates: Coordinates
    address: Address
    offer_type: Optional[str]

    characteristics: Characteristics
    

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

def extract_json_with_key(text: str, key: str) -> JsonType | None:

    count = 0
    # initial key search
    start_index = text.find(key)
    if start_index == -1:
        return None
    
    # Now find the first '{' after the key
    brace_start = text.find("{", start_index)
    if brace_start == -1:
        return None
    
    brace_end = brace_start
    # count curly braces
    for i, char in enumerate(text[brace_start:], start=brace_start):
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        if count == 0:
            brace_end = i
            break
    
    # decode
    if brace_end > start_index:
        json_str = text[brace_start:brace_end + 1]
        try:
            json_obj = json.loads(json_str)
            return json_obj
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON string: {json_str}")
            return None
    
    return None

def preprocess_json(json: JsonType) -> None:
    if isinstance(json, dict):
        characteristics_list = json.get("characteristics", None)
        if isinstance(characteristics_list, list):
            characteristics = {str(item["key"]): item['value'] for item in characteristics_list if isinstance(item, dict) and item.get("key") and item.get("value")}
            json["characteristics"] = characteristics
            
        features_list = json.get("features", None)
        if isinstance(features_list, list):
            json["features"] = ",".join(str(f) for f in features_list)
        

async def parse_offer(content: DocContent) -> Offer | None:
    sel = Selector(text=content)
    canonical: str | None = sel.xpath('//link[@rel="canonical"]/@href').get()
    offer_id: str | None = get_offer_id_from_url("OTO", Url(canonical))

    if not offer_id:
        logger.warning(f"Offer ID not found in {canonical}.")
        return None

    key_to_search = '"ad":{'
    json_raw = extract_json_with_key(content, key_to_search)
    
    if json_raw is None:
        logger.warning(f"JSON object with tag `{key_to_search}` not found in {canonical}.")
        return None

    preprocess_json(json_raw)
    ad = msgspec.convert(json_raw, type=Ad)
        
    
    
    # characteristics_list = ad.get("characteristics", [])
    # characteristics = {item["key"]: item for item in characteristics_list if "key" in item and "value" in item}

    
    
    logger.info(f"Parsed ad: {ad}")
    # offer = Offer(
    #     id=get_safe_nested(ad, ["id"], ""),
    #     title=get_safe_nested(ad, ["title"], ""),
    #     features=",".join(get_safe_nested(ad, ["features"], [])),
    #     description=html.unescape(get_safe_nested(ad, ["description"], "")),
    #     url=get_safe_nested(ad, ["url"], None),
    #     latitude=get_safe_nested(coordinates, ["latitude"], None),
    #     longitude=get_safe_nested(coordinates, ["longitude"], None),
    #     province=get_safe_nested(address, ["province", "name"], None),
    #     city=get_safe_nested(address, ["city", "name"], None),
    #     subregion=get_safe_nested(address, ["county", "name"], None),
    #     district=get_safe_nested(address, ["district", "name"], None),
    #     street=get_safe_nested(address, ["street", "name"], None),

    #     offer_type=get_safe_nested(ad, ["adCategory", "type"], None),

    #     price = get_safe_nested(characteristics, ["price", "value"], 0),
    #     size = get_safe_nested(characteristics, ["m", "value"], 0),
    #     rooms = get_safe_nested(characteristics, ["rooms_num", "value"], None),
    #     market_type=get_safe_nested(characteristics, ["market", "value"], None),
    #     building_type=get_safe_nested(characteristics, ["building_type", "value"], None),
    #     floor_number=get_safe_nested(characteristics, ["floor_no", "value"], None),
    #     building_floors_num=get_safe_nested(characteristics, ["building_floors_num", "value"], None),
    #     material=get_safe_nested(characteristics, ["building_material", "value"], None),
    #     window_type=get_safe_nested(characteristics, ["windows_type", "value"], None),
    #     heating=get_safe_nested(characteristics, ["heating", "value"], ""),
    #     year_built=get_safe_nested(characteristics, ["build_year", "value"], None),
    #     rent=get_safe_nested(characteristics, ["rent", "value"], None),
    #     ownership=get_safe_nested(characteristics, ["building_ownership", "value"], None),
    #     construction_status=get_safe_nested(characteristics, ["construction_status", "value"], None),
    # )

    
    # logger.info(f"Json data: {offer}")
    # return offer


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
