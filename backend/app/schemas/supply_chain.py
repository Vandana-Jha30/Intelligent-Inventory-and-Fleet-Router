from pydantic import BaseModel, Field

from app.schemas.inventory import InventoryForecastAnalysisResponse
from app.schemas.min_cost_flow import MinCostFlowResponse
from app.schemas.vehicle_routing import VehicleRoutingResponse


class SupplyChainPlanRequest(BaseModel):
    """Inputs for an integrated inventory + distribution plan.

    Inventory replenishment is evaluated independently from customer
    distribution. Delivery locations use their persisted demand_quantity.
    """

    product_id: int = Field(gt=0)
    warehouse_id: int = Field(gt=0)
    depot_id: int = Field(gt=0)
    window: int = Field(default=3, ge=1)
    delivery_location_ids: list[int] | None = Field(
        default=None,
        min_length=1,
    )


class SupplyChainAllocationResponse(BaseModel):
    warehouse_id: int
    warehouse_name: str
    location_id: int
    location_name: str
    quantity: float
    distance_km: float
    transportation_cost: float


class WarehouseAllocationResponse(BaseModel):
    warehouse_id: int
    warehouse_name: str
    location_id: int
    location_name: str
    quantity: float
    distance_km: float
    transportation_cost: float


class BaselineAllocationResponse(BaseModel):
    total_cost: float
    total_flow: float
    allocation: list[WarehouseAllocationResponse]


class SupplyChainPlanResponse(BaseModel):
    product_id: int
    warehouse_id: int
    depot_id: int
    delivery_demand: float
    available_inventory: float
    inventory_analysis: InventoryForecastAnalysisResponse
    min_cost_flow: MinCostFlowResponse
    allocation: list[SupplyChainAllocationResponse]
    baseline_allocation: BaselineAllocationResponse
    baseline_cost: float
    optimized_cost: float
    cost_improvement_percent: float
    routing: VehicleRoutingResponse


