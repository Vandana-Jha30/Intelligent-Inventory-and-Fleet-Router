from pydantic import BaseModel


class VehicleRoutingRequest(BaseModel):
    depot_id: int


class VehicleRoutingRouteResponse(BaseModel):
    vehicle_id: int
    location_ids: list[int]
    total_demand: float
    remaining_capacity: float
    route_distance: float
    route_cost: float


class VehicleRoutingResponse(BaseModel):
    total_distance: float
    total_cost: float
    routes: list[VehicleRoutingRouteResponse]