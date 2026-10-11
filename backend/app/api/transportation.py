from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.transportation import (
    TransportationRequest,
    TransportationResponse
)

from app.services.transportation_service import (
    solve_transportation_plan
)


router = APIRouter(
    prefix="/api/transportation",
    tags=["Transportation"]
)


@router.post(
    "/solve",
    response_model=TransportationResponse
)
def solve(
    request: TransportationRequest,
    db: Session = Depends(get_db)
):
    try:

        return solve_transportation_plan(
            db=db,
            warehouse_ids=request.warehouse_ids,
            delivery_location_ids=request.delivery_location_ids
        )

    except ValueError as error:

        message = str(error)

        # Missing warehouse/location is a
        # resource-not-found condition.
        if (
            message.startswith("Warehouse not found")
            or
            message.startswith("Delivery location not found")
        ):
            raise HTTPException(
                status_code=404,
                detail=message
            )

        # Everything else is a bad request.
        raise HTTPException(
            status_code=400,
            detail=message
        )