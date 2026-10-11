from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.warehouse import Warehouse
from app.models.delivery_location import DeliveryLocation

from app.optimization.facility_location_optimizer import (
    solve_facility_location
)

from app.schemas.facility_location import (
    FacilityLocationRequest,
    FacilityLocationResponse
)


router = APIRouter(
    prefix="/api/facility-location",
    tags=["Facility Location"]
)


@router.post(
    "/solve",
    response_model=FacilityLocationResponse
)
def solve_facility_location_api(
    request: FacilityLocationRequest,
    db: Session = Depends(get_db)
):
    # Validate duplicate IDs

    if len(request.warehouse_ids) != len(
        set(request.warehouse_ids)
    ):
        raise HTTPException(
            status_code=400,
            detail="Each warehouse ID can appear only once"
        )

    if len(request.delivery_location_ids) != len(
        set(request.delivery_location_ids)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Each delivery location ID can appear only once"
            )
        )

    # Fetch warehouses

    warehouses = db.query(Warehouse).filter(
        Warehouse.warehouse_id.in_(
            request.warehouse_ids
        )
    ).all()

    warehouse_map = {
        warehouse.warehouse_id: warehouse
        for warehouse in warehouses
    }

    missing_warehouse_ids = [
        warehouse_id
        for warehouse_id in request.warehouse_ids
        if warehouse_id not in warehouse_map
    ]

    # IMPORTANT:
    # Check missing warehouses first.
    # This matches the API test expectations.

    if missing_warehouse_ids:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Warehouse not found: "
                f"{missing_warehouse_ids[0]}"
            )
        )

    # Fetch delivery locations

    delivery_locations = db.query(
        DeliveryLocation
    ).filter(
        DeliveryLocation.location_id.in_(
            request.delivery_location_ids
        )
    ).all()

    location_map = {
        location.location_id: location
        for location in delivery_locations
    }

    missing_location_ids = [
        location_id
        for location_id in request.delivery_location_ids
        if location_id not in location_map
    ]

    if missing_location_ids:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Delivery location not found: "
                f"{missing_location_ids[0]}"
            )
        )

    # Preserve requested order

    warehouses = [
        warehouse_map[warehouse_id]
        for warehouse_id in request.warehouse_ids
    ]

    delivery_locations = [
        location_map[location_id]
        for location_id in request.delivery_location_ids
    ]

    # Solve

    try:
        result = solve_facility_location(
            candidate_warehouses=warehouses,
            delivery_locations=delivery_locations
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    return result