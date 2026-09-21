from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.vehicle_routing import (
    VehicleRoutingRequest,
    VehicleRoutingResponse
)


from app.services.vehicle_routing_service import (
    solve_routing,
    compare_routing
)


router = APIRouter(
    prefix="/api/vehicle-routing",
    tags=["Vehicle Routing"]
)


@router.post(
    "/solve",
    response_model=VehicleRoutingResponse
)
def solve(
    request: VehicleRoutingRequest,
    db: Session = Depends(get_db)
):
    try:

        return solve_routing(
            db,
            request.depot_id
        )

    except ValueError as error:

        message = str(error)

        if message == "Depot not found":
            raise HTTPException(
                status_code=404,
                detail=message
            )

        raise HTTPException(
            status_code=400,
            detail=message
        )



@router.post(
    "/compare"
)
def compare(
    request: VehicleRoutingRequest,
    db: Session = Depends(get_db)
):
    try:

        return compare_routing(
            db,
            request.depot_id
        )

    except ValueError as error:

        message = str(error)

        if message == "Depot not found":
            raise HTTPException(
                status_code=404,
                detail=message
            )

        raise HTTPException(
            status_code=400,
            detail=message
        )