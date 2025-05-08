import json
from typing import Dict, List, Union

from loguru import logger
import msgspec
from parsel import Selector
from common.classes import DocContent, Url
from common.utils import get_offer_id_from_url
from db.models import Offer
from html_parser.OTO_msgspec import Ad

JsonType = Union[None, int, str, bool, List['JsonType'], Dict[str, 'JsonType']]

def convert_msgspec_to_db_model(json_obj: Ad) -> Offer:
    """Convert a msgspec object to a database model."""
    
def extract_json_with_key(text: str, key: str) -> str | None:

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
    json_string = extract_json_with_key(content, key_to_search)
    
    if json_string is None:
        logger.warning(f"JSON object with tag `{key_to_search}` not found in {canonical}.")
        return None

    offer_data = msgspec.json.decode(json_string, type=Ad)
    offer = convert_msgspec_to_db_model(offer_data)
    # logger.info(f"Parsed ad: {offer_data}")
    return offer