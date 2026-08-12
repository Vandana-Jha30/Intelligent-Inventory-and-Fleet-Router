from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    unit_cost: float
    ordering_cost: float
    holding_cost: float
    lead_time_days: int
    service_level: float


class ProductResponse(BaseModel):
    product_id: int
    sku: str
    name: str
    unit_cost: float
    ordering_cost: float
    holding_cost: float
    lead_time_days: int
    service_level: float

    class Config:
        from_attributes = True