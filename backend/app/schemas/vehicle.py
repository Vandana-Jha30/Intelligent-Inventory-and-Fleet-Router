from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    vehicle_number: str
    capacity: float
    fixed_cost: float = 0
    cost_per_km: float


class VehicleResponse(BaseModel):
    vehicle_id: int
    vehicle_number: str
    capacity: float
    fixed_cost: float
    cost_per_km: float

    model_config = ConfigDict(from_attributes=True)