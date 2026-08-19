from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse
)

from app.services.vehicle_service import (
    create_vehicle,
    get_vehicles,
    get_vehicle,
    update_vehicle,
    delete_vehicle
)


router = APIRouter(
    prefix="/api/vehicles",
    tags=["Vehicles"]
)


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=201
)
def create(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_vehicle(db, vehicle_data)

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get(
    "",
    response_model=list[VehicleResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_vehicles(db)


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def get_one(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = get_vehicle(db, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def update(
    vehicle_id: int,
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):
    try:
        vehicle = update_vehicle(
            db,
            vehicle_id,
            vehicle_data
        )

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found"
            )

        return vehicle

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.delete("/{vehicle_id}")
def delete(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_vehicle(
        db,
        vehicle_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return {
        "message": "Vehicle deleted successfully"
    }