from pydantic import BaseModel, ConfigDict, Field   


class InventoryCreate(BaseModel):
    warehouse_id: int = Field(gt=0)
    product_id: int = Field(gt=0)

    on_hand: int = Field(ge=0)
    reserved: int = Field(default=0, ge=0)
    on_order: int = Field(default=0, ge=0)


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


class InventoryForecastAnalysisResponse(BaseModel):
    product_id: int
    warehouse_id: int

    forecast_daily_demand: float
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