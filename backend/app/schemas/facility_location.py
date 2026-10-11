from pydantic import BaseModel, Field


class FacilityLocationRequest(BaseModel):

    warehouse_ids: list[int] = Field(
        min_length=1
    )

    delivery_location_ids: list[int] = Field(
        min_length=1
    )


class OpenedFacilityResponse(BaseModel):

    warehouse_id: int
    warehouse_name: str
    fixed_opening_cost: float
    capacity: float


class AllocationResponse(BaseModel):

    warehouse_id: int
    location_id: int
    quantity: float
    distance: float
    transportation_cost: float


class FacilitySummaryResponse(BaseModel):

    warehouse_id: int
    opened: bool
    capacity: float
    assigned_quantity: float
    remaining_capacity: float


class FacilityLocationResponse(BaseModel):

    total_demand: float
    facilities_opened: int
    total_fixed_cost: float
    total_transportation_cost: float
    total_cost: float

    opened_facilities: list[
        OpenedFacilityResponse
    ]

    allocation_plan: list[
        AllocationResponse
    ]

    facility_summary: list[
        FacilitySummaryResponse
    ]