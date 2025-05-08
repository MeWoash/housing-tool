from sqlmodel import SQLModel, Field

class Offer(SQLModel, table=True):
    id: str = Field(primary_key=True)
    price: int
    size: int
    title: str | None = None
    rooms: int | None = None
    year_built: int | None = None
    heating: str | None = None
    building_type: str | None = None
    material: str | None = None
    rent: int | None = None
    ownership: str | None = None
    features: str | None = None
    floor_number: int | None = None
    market_type: str | None = None
    offer_type: str | None = None
    window_type: str | None = None
    description: str | None = None
    url: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    province: str | None = None
    city: str | None = None
    subregion: str | None = None
    building_floors_num: int | None = None
    construction_status: str | None = None
    district: str | None = None
    street: str | None = None

    def __str__(self) -> str:
        return f"Offer(id={self.id}, title={self.title}, price={self.price}, size={self.size}, url={self.url})"
