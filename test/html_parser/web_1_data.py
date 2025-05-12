

WEB_1_VALID_JSON = r"""
"ad":{
    "description": "\\u003cbr/\\u003e\\r\\n \\u003cbr/\\u003e\\r\\n\\u003cbr/\\u003e\\r\\nN\\u003cstrong\\u003ea sprzedaż 2-pokojowe mieszkanie po generalnym remoncie.",
    "features": [
        "internet",
        "piwnica",
        "oddzielna kuchnia",
        "winda"
    ],
    "title": "2 Pokoje |PO Generalnym Remoncie | Pomorzany!",
    "url": "https://simple-site/some-text-ID12345",
    "characteristics": [
        {
            "key": "price",
            "value": "419000",
            "label": "Cena",
            "localizedValue": "419 000 zł",
            "currency": "PLN",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "m",
            "value": "37",
            "label": "Powierzchnia",
            "localizedValue": "37 m²",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "price_per_m",
            "value": "11324",
            "label": "cena za metr",
            "localizedValue": "11 324 zł/m²",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "rooms_num",
            "value": "2",
            "label": "Liczba pokoi",
            "localizedValue": "2",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "market",
            "value": "secondary",
            "label": "Rynek",
            "localizedValue": "wtórny",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "building_type",
            "value": "block",
            "label": "Rodzaj zabudowy",
            "localizedValue": "blok",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "floor_no",
            "value": "floor_1",
            "label": "Piętro",
            "localizedValue": "1",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "building_floors_num",
            "value": "4",
            "label": "Liczba pięter",
            "localizedValue": "4",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "windows_type",
            "value": "plastic",
            "label": "Okna",
            "localizedValue": "plastikowe",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "heating",
            "value": "urban",
            "label": "Ogrzewanie",
            "localizedValue": "miejskie",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "build_year",
            "value": "1974",
            "label": "Rok budowy",
            "localizedValue": "1974",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "construction_status",
            "value": "ready_to_use",
            "label": "Stan wykończenia",
            "localizedValue": "do zamieszkania",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "rent",
            "value": "500",
            "label": "Czynsz",
            "localizedValue": "500 zł",
            "currency": "PLN",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "building_ownership",
            "value": "full_ownership",
            "label": "Forma własności",
            "localizedValue": "pełna własność",
            "currency": "",
            "suffix": "",
            "__typename": "Characteristic"
        },
        {
            "key": "price_per_m",
            "value": "11378.38"
        }
    ],
    "location": {
        "coordinates": {
            "latitude": 53.406439,
            "longitude": 14.5283
        },
        "address": {
            "street": null,
            "district": {
                "id": "159",
                "code": "pomorzany",
                "name": "Pomorzany"
            },
            "city": {
                "id": "213",
                "code": "szczecin",
                "name": "Szczecin"
            },
            "subregion": null,
            "province": {
                "id": "16",
                "code": "zachodniopomorskie",
                "name": "zachodniopomorskie"
            }
        }
    }
}
"""

WEB_1_NONE_JSON = r"""
"ad":{
    "title": "2 Pokoje |PO Generalnym Remoncie | Pomorzany!",
    "url": "https://simple-site/some-text-ID12345",
    "characteristics": [
        {
            "key": "price",
            "value": "419000",
            "label": "Cena",
            "localizedValue": "419 000 zł",
            "currency": "PLN",
            "suffix": "",
            "__typename": "Characteristic"
        }
    ],
    "location": {
    }
}
"""

WEB_1_NO_URL_JSON = r"""
"ad":{
    "title": "2 Pokoje |PO Generalnym Remoncie | Pomorzany!",
    "characteristics": [
        {
            "key": "price",
            "value": "419000",
            "label": "Cena",
            "localizedValue": "419 000 zł",
            "currency": "PLN",
            "suffix": "",
            "__typename": "Characteristic"
        }
    ],
    "location": {
    }
}
"""