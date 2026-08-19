from pydantic import BaseModel, ConfigDict, Field


class DepotCreate(BaseModel):
    depot_name: str = Field(
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


class DepotResponse(BaseModel):
    depot_id: int
    depot_name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)