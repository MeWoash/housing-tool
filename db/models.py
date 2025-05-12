from sqlmodel import SQLModel, Field

class Offer(SQLModel, table=True):
    id: str = Field(primary_key=True)
    price: float | None
    size: float | None
    title: str | None
    rooms: int | None
    year_built: int | None
    heating: str | None
    building_type: str | None
    material: str | None
    rent: float | None
    ownership: str | None
    features: str | None
    floor_number: int | None
    market_type: str | None
    window_type: str | None
    description: str | None
    latitude: float | None
    longitude: float | None
    province: str | None
    city: str | None
    subregion: str | None
    building_floors_num: int | None
    construction_status: str | None
    district: str | None
    street: str | None
    url: str | None
    price_per_m: float | None

    def __str__(self) -> str:
        return f"Offer(id={self.id}, price={self.price}, size={self.size}, title={self.title}, url={self.url})"

    def __repr__(self) -> str:
        return f"Offer(id={self.id}, price={self.price}, size={self.size}, title={self.title}, url={self.url})"