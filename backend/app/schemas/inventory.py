from pydantic import BaseModel, ConfigDict


class InventoryCreate(BaseModel):
    warehouse_id: int
    product_id: int
    on_hand: int
    reserved: int = 0
    on_order: int = 0


class InventoryResponse(BaseModel):
    inventory_id: int
    warehouse_id: int
    product_id: int
    on_hand: int
    reserved: int
    on_order: int

    model_config = ConfigDict(from_attributes=True)


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
    recommended_order_quantity: float