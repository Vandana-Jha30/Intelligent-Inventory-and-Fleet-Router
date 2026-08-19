from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.delivery_location import (
    DeliveryLocationCreate,
    DeliveryLocationResponse
)

from app.services.delivery_location_service import (
    create_delivery_location,
    get_delivery_locations,
    get_delivery_location,
    update_delivery_location,
    delete_delivery_location
)


router = APIRouter(
    prefix="/api/delivery-locations",
    tags=["Delivery Locations"]
)


@router.post(
    "",
    response_model=DeliveryLocationResponse,
    status_code=201
)
def create(
    location_data: DeliveryLocationCreate,
    db: Session = Depends(get_db)
):
    return create_delivery_location(
        db,
        location_data
    )


@router.get(
    "",
    response_model=list[DeliveryLocationResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_delivery_locations(db)


@router.get(
    "/{location_id}",
    response_model=DeliveryLocationResponse
)
def get_one(
    location_id: int,
    db: Session = Depends(get_db)
):
    location = get_delivery_location(
        db,
        location_id
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Delivery location not found"
        )

    return location


@router.put(
    "/{location_id}",
    response_model=DeliveryLocationResponse
)
def update(
    location_id: int,
    location_data: DeliveryLocationCreate,
    db: Session = Depends(get_db)
):
    location = update_delivery_location(
        db,
        location_id,
        location_data
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Delivery location not found"
        )

    return location


@router.delete(
    "/{location_id}"
)
def delete(
    location_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_delivery_location(
        db,
        location_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Delivery location not found"
        )

    return {
        "message": "Delivery location deleted successfully"
    }