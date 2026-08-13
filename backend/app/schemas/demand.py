from datetime import date

from pydantic import BaseModel, ConfigDict


class DemandCreate(BaseModel):
    product_id: int
    warehouse_id: int
    demand_date: date
    quantity: int


class DemandResponse(BaseModel):
    demand_id: int
    product_id: int
    warehouse_id: int
    demand_date: date
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class DemandForecastResponse(BaseModel):
    product_id: int
    warehouse_id: int
    method: str
    window: int
    forecast: float