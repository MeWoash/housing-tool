from typing import Optional
import msgspec

class Coordinates(msgspec.Struct):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressElement(msgspec.Struct):
    id : Optional[str] = None
    code : Optional[str] = None
    name : Optional[str] = None
    number : Optional[str] = None
    province: Optional[str] = msgspec.field(name="__province", default=None)

class Address(msgspec.Struct):
    province: Optional[AddressElement] = None
    city: Optional[AddressElement] = None
    subregion: Optional[AddressElement] = None
    district: Optional[AddressElement] = None
    street: Optional[AddressElement] = None

class Location(msgspec.Struct):
    coordinates: Optional[Coordinates] = None
    address: Optional[Address] = None

# price, size, rooms, market_type, building_type, floor_number, building_floors_num, material, window_type, heating, year_built, rent, ownership, construction_status
class CharacteristicElement(msgspec.Struct):
    key: Optional[str] = None
    value: Optional[str] = None
    label: Optional[str] = None
    localizedValue: Optional[str] = None
    currency: Optional[str] = None
    suffix: Optional[str] = None
    typename: Optional[str] = msgspec.field(name="__typename", default=None)


class Ad(msgspec.Struct):
    url: str
    title: Optional[str] = None
    features: Optional[list[str]] = None
    description: Optional[str] = None
    characteristics: Optional[list[CharacteristicElement]] = None

    location: Optional[Location] = None
    offer_type: Optional[str] = None