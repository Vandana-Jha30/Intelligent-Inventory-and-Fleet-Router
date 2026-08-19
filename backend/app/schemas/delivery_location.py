from pydantic import BaseModel, ConfigDict, Field


class DeliveryLocationCreate(BaseModel):
    location_name: str = Field(
        min_length=1,
        max_length=100
    )

    latitude: float = Field(
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ge=-180,
        le=180
    )

    demand_quantity: float = Field(
        ge=0
    )


class DeliveryLocationResponse(BaseModel):
    location_id: int
    location_name: str
    latitude: float
    longitude: float
    demand_quantity: float

    model_config = ConfigDict(from_attributes=True)