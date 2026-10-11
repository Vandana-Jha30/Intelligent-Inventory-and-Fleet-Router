from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TransportationRequest(BaseModel):
    warehouse_ids: Optional[List[int]] = None
    delivery_location_ids: Optional[List[int]] = None


class ShipmentPlanItem(BaseModel):
    warehouse_id: int
    location_id: int
    quantity: float
    distance: float
    transportation_cost: float


class WarehouseTransportationSummary(BaseModel):
    warehouse_id: int
    available_supply: float
    shipped_quantity: float
    remaining_supply: float


class TransportationResponse(BaseModel):
    total_supply: float
    total_demand: float
    total_transportation_cost: float

    shipment_plan: List[ShipmentPlanItem]

    warehouse_summary: List[
        WarehouseTransportationSummary
    ]