from pydantic import BaseModel


class InventoryAnalysisResponse(BaseModel):
    product_id: int
    warehouse_id: int

    average_daily_demand: float
    annual_demand: float
    demand_std: float

    eoq: float
    safety_stock: float
    reorder_point: float

    on_hand: int
    reserved: int
    on_order: int
    inventory_position: int

    replenishment_required: bool