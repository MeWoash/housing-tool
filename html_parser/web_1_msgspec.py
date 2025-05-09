import msgspec

class Coordinates(msgspec.Struct, frozen = True):
    latitude: float | None = None
    longitude: float | None = None

class AddressElement(msgspec.Struct, frozen = True):
    name : str | None = None
    id : str | None = None
    code : str | None = None
    number : str | None = None
    province: str | None = msgspec.field(name="__province", default=None)

class Address(msgspec.Struct):
    province: AddressElement | None = None
    city: AddressElement | None = None
    subregion: AddressElement | None = None
    district: AddressElement | None = None
    street: AddressElement | None = None

class Location(msgspec.Struct):
    coordinates: Coordinates | None = None
    address: Address | None = None
# price, size, rooms, market_type, building_type, floor_number, building_floors_num, material, window_type, heating, year_built, rent, ownership, construction_status
class CharacteristicElement(msgspec.Struct):
    key: str
    value: str
    label: str | None = None
    localizedValue: str | None = None
    currency: str| None = None
    suffix: str | None = None
    typename: str | None = msgspec.field(name="__typename", default=None)


class Ad(msgspec.Struct):
    url: str
    title: str
    location: Location
    characteristics: list[CharacteristicElement]
    features: list[str] | None = None
    description: str | None = None
