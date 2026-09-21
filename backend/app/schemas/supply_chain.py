from pydantic import BaseModel, Field

from app.schemas.inventory import InventoryForecastAnalysisResponse
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
    delivery_location_ids: list[int] | None = Field(default=None, min_length=1)


class SupplyChainPlanResponse(BaseModel):
    product_id: int
    warehouse_id: int
    depot_id: int
    delivery_demand: float
    inventory_analysis: InventoryForecastAnalysisResponse
    routing: VehicleRoutingResponse

