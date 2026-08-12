from datetime import date

from pydantic import BaseModel


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

    class Config:
        from_attributes = True