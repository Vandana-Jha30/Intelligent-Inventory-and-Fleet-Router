from pydantic import BaseModel


class WarehouseCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    capacity: int
    operating_cost: float


class WarehouseResponse(BaseModel):
    warehouse_id: int
    name: str
    latitude: float
    longitude: float
    capacity: int
    operating_cost: float

    class Config:
        from_attributes = True