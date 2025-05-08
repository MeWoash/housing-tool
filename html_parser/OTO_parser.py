import json
from typing import List, Union

from loguru import logger
import msgspec
from parsel import Selector
from common.classes import DocContent, Url
from common.utils import get_offer_id_from_url
from db.models import Offer
from html_parser.OTO_msgspec import Ad, CharacteristicElement
import re

JsonType = Union[None, int, str, bool, List['JsonType'], dict[str, 'JsonType']]


def extract_characteristics(characteristics: list[CharacteristicElement]) -> dict[str, str]:
    return {c.key: c.value for c in characteristics}

def strip_html_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"(\\r\\n|\\n|\\r)+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def convert_msgspec_to_db_model(json_obj: Ad) -> Offer | None:
    """Convert a msgspec object to a database model."""
    characteristics_dict= extract_characteristics(json_obj.characteristics)

    
    floor_no_str = characteristics_dict.get("floor_no", "-1")
    floor_match = re.search(r'\d+', floor_no_str)
    floor_number = int(floor_match.group()) if floor_match else None

    id = get_offer_id_from_url("OTO", Url(json_obj.url))
    if id is False:
        return None
    id = str(id)

    building_floors_num = int(characteristics_dict.get("building_floors_num", 0)) or None
    construction_status = characteristics_dict.get("construction_status", None)
    price = float(characteristics_dict.get("price", 0) or 0) or None
    size = float(characteristics_dict.get("m", 0)) or None
    rooms = int(characteristics_dict.get("rooms", 0)) or None
    year_built = int(characteristics_dict.get("year_built", 0)) or None
    heating = characteristics_dict.get("heating", None)
    building_type = characteristics_dict.get("building_type", None)
    material = characteristics_dict.get("material", None)
    rent = float(characteristics_dict.get("rent", 0)) or None
    ownership = characteristics_dict.get("ownership", None)
    floor_number = floor_number
    market_type = characteristics_dict.get("market_type", "")
    window_type = characteristics_dict.get("window_type", "")
    title = json_obj.title or None
    features = "".join(json_obj.features or []) or None
    description = strip_html_tags(json_obj.description) if json_obj.description else None
    url = json_obj.url

    latitude = None
    longitude = None
    if json_obj.location.coordinates:
        latitude = json_obj.location.coordinates.latitude
        longitude = json_obj.location.coordinates.latitude

    address = json_obj.location.address
    province = None
    city = None
    subregion = None
    district = None
    street = None
    if address:
        if address.province:
            province = address.province.name
        if address.city:
            city = address.city.name
        if address.subregion:
            subregion = address.subregion.name
        if address.district:
            district = address.district.name
        if address.street:
            street = address.street.name
    
    offer = Offer(
        id = id,
        building_floors_num = building_floors_num,
        construction_status = construction_status,
        price = price,
        size = size,
        rooms = rooms,
        year_built = year_built,
        heating = heating,
        building_type = building_type,
        material = material,
        rent = rent,
        ownership = ownership,
        floor_number = floor_number,
        market_type = market_type,
        window_type = window_type,
        title = title,
        features = features,
        description = description,
        url = url,
        latitude = latitude,
        longitude = longitude,
        province = province,
        city = city,
        subregion = subregion,
        district = district,
        street = street) 

    return offer
    
async def extract_json_with_key(text: str, key: str) -> str | None:

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
            _ = json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON string: {json_str}")
            return None
    
    return None

async def OTO_parse_offer(content: DocContent) -> Offer | None:
    sel = Selector(text=content)
    canonical: str | None = sel.xpath('//link[@rel="canonical"]/@href').get()
    offer_id: str | None = get_offer_id_from_url("OTO", Url(canonical))

    if not offer_id:
        logger.warning(f"Offer ID not found in {canonical}.")
        return None

    key_to_search = '"ad":{'
    json_string = await extract_json_with_key(content, key_to_search)
    
    if json_string is None:
        logger.warning(f"JSON object with tag `{key_to_search}` not found in {canonical}.")
        return None

    try:
        offer_data = msgspec.json.decode(json_string, type=Ad)
    except msgspec.DecodeError as e:
        logger.exception(f"Failed to decode JSON: {e}")
        return None
    
    try:
        offer = convert_msgspec_to_db_model(offer_data)
    except Exception as e:
        logger.exception(f"Error while converting msgspec to db model: {e}")
        return None
    
    return offer