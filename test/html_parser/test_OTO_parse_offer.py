from typing import ContextManager, Any, Tuple
import pytest
from common.classes import DocContent
from db.models import Offer
from html_parser.OTO_parser import OTO_parse_offer
from test.html_parser.test_OTO_data import OTO_VALID_JSON, OTO_NONE_JSON, OTO_NO_URL_JSON
from contextlib import nullcontext


def assert_offers_equal(expected: Offer | None, actual: Offer | None) -> None:
    """
    Assert that all public attributes of two Offer instances are equal.
    """
    if expected is None and actual is None:
        return # Both are None, so they are equal
    
    if not isinstance(expected, Offer) or not isinstance(actual, Offer):
        assert False, (f"Expected Offer instance, got {type(expected).__name__} and {type(actual).__name__}")

    # Collect all non-private attributes from the expected offer
    attrs = [name for name in vars(expected) if not name.startswith("_")]
    for attr in attrs:
        val_exp = getattr(expected, attr)
        val_act = getattr(actual, attr)
        assert val_exp == val_act, (
            f"Attribute '{attr}' mismatch: "
            f"expected={val_exp!r}, actual={val_act!r}"
        )

TestVType = list[Tuple[DocContent, ContextManager[Any], Offer | None]]


TEST_VECTOR: TestVType = [
    # ITER 1
    (
        DocContent(OTO_VALID_JSON),
        nullcontext(),
        Offer(
            id="OTO_12345",
            price=419000.0,
            size=37.0,
            title="2 Pokoje |PO Generalnym Remoncie | Pomorzany!",
            rooms=2,
            year_built=1974,
            heating="urban",
            building_type="block",
            material=None,
            rent=500.0,
            ownership="full_ownership",
            features="internet,piwnica,oddzielna kuchnia,winda",
            floor_number=1,
            market_type="secondary",
            window_type="plastic",
            description="N a sprzedaż 2-pokojowe mieszkanie po generalnym remoncie.",
            latitude=53.406439,
            longitude=14.5283,
            province="zachodniopomorskie",
            city="Szczecin",
            subregion=None,
            building_floors_num=4,
            construction_status="ready_to_use",
            district="Pomorzany",
            street=None,
            url="https://www.otodom.pl/pl/oferta/some-text-ID12345"
        )
    ),
    # ITER 2
    (
        DocContent(OTO_NONE_JSON),
        nullcontext(),
        Offer(
            id="OTO_12345",
            price=419000.0,
            size=None,
            title="2 Pokoje |PO Generalnym Remoncie | Pomorzany!",
            rooms=None,
            year_built=None,
            heating=None,
            building_type=None,
            material=None,
            rent=None,
            ownership=None,
            features=None,
            floor_number=None,
            market_type=None,
            window_type=None,
            description=None,
            latitude=None,
            longitude=None,
            province=None,
            city=None,
            subregion=None,
            building_floors_num=None,
            construction_status=None,
            district=None,
            street=None,
            url="https://www.otodom.pl/pl/oferta/some-text-ID12345"
        )
    ),
    # ITER 3
    (
        DocContent(OTO_NO_URL_JSON),
        nullcontext(),
        None
    )
]


@pytest.mark.asyncio
@pytest.mark.parametrize("doc_content, expectation, expected_offer", TEST_VECTOR)
async def test_OTO_parse_offer(
    doc_content: DocContent,
    expectation: ContextManager[Any],
    expected_offer: Offer | None) -> None:

    with expectation:
        # The 'offer' parameter from parametrize is the expected offer.
        # The result of OTO_parse_offer is the actual offer.
        actual_offer = await OTO_parse_offer(doc_content)
        assert_offers_equal(expected=expected_offer, actual=actual_offer)




