from sqlmodel import SQLModel, Field

class Offer(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str | None = None
    price: str | None = None
    size: str | None = None
    rooms: str | None = None
    year_built: str | None = None
    heating: str | None = None
    building_type: str | None = None
    material: str | None = None
    rent: str | None = None
    ownership: str | None = None
    condition: str | None = None
    elevator: bool = False
    media: str | None = None
    source: str | None = None
    heating_type: str | None = None
    floor_number: str | None = None
    maintenance_cost: str | None = None
    finishing_state: str | None = None
    market_type: str | None = None
    ownership_type: str | None = None
    advertiser_type: str | None = None
    additional_info: str | None = None
    construction_year: str | None = None
    has_elevator: str | None = None
    building_type_detail: str | None = None
    window_type: str | None = None
    security: str | None = None
    safety_features: str | None = None
    media: str | None = None
    description: str | None = None
    url: str | None = None

    def __str__(self) -> str:
        return (
            f"Offer(id={self.id}, title={self.title}, price={self.price}, "
            f"year_built={self.year_built}, building_type={self.building_type}, "
            f"heating={self.heating}, rent={self.rent}, ownership={self.ownership}, "
            f"condition={self.condition}, elevator={self.elevator}, material={self.material}, "
            f"media={self.media}, source={self.source}, "
            f"heating_type={self.heating_type}, floor_number={self.floor_number}, "
            f"maintenance_cost={self.maintenance_cost}, finishing_state={self.finishing_state}, "
            f"market_type={self.market_type}, ownership_type={self.ownership_type}, "
            f"advertiser_type={self.advertiser_type}, additional_info={self.additional_info}, "
            f"construction_year={self.construction_year}, has_elevator={self.has_elevator}, "
            f"building_type_detail={self.building_type_detail}, window_type={self.window_type}, "
            f"security={self.security}, safety_features={self.safety_features}, "
            f"media={self.media}, description={bool(self.description)}), "
            f"url={self.url}"
        )