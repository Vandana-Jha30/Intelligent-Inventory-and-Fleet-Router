from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.depot import (
    DepotCreate,
    DepotResponse
)

from app.services.depot_service import (
    create_depot,
    get_depots,
    get_depot,
    update_depot,
    delete_depot
)


router = APIRouter(
    prefix="/api/depots",
    tags=["Depots"]
)


@router.post(
    "",
    response_model=DepotResponse,
    status_code=201
)
def create(
    depot_data: DepotCreate,
    db: Session = Depends(get_db)
):
    return create_depot(
        db,
        depot_data
    )


@router.get(
    "",
    response_model=list[DepotResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_depots(db)


@router.get(
    "/{depot_id}",
    response_model=DepotResponse
)
def get_one(
    depot_id: int,
    db: Session = Depends(get_db)
):
    depot = get_depot(
        db,
        depot_id
    )

    if depot is None:
        raise HTTPException(
            status_code=404,
            detail="Depot not found"
        )

    return depot


@router.put(
    "/{depot_id}",
    response_model=DepotResponse
)
def update(
    depot_id: int,
    depot_data: DepotCreate,
    db: Session = Depends(get_db)
):
    depot = update_depot(
        db,
        depot_id,
        depot_data
    )

    if depot is None:
        raise HTTPException(
            status_code=404,
            detail="Depot not found"
        )

    return depot


@router.delete(
    "/{depot_id}"
)
def delete(
    depot_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_depot(
        db,
        depot_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Depot not found"
        )

    return {
        "message": "Depot deleted successfully"
    }