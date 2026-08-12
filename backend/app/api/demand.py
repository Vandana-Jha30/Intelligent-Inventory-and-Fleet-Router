from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.demand import (
    DemandCreate,
    DemandResponse
)

from app.services.demand_service import (
    create_demand,
    get_demands,
    get_demand,
    delete_demand
)


router = APIRouter(
    prefix="/api/demand",
    tags=["Demand History"]
)


@router.post(
    "",
    response_model=DemandResponse
)
def create(
    demand_data: DemandCreate,
    db: Session = Depends(get_db)
):
    return create_demand(db, demand_data)


@router.get(
    "",
    response_model=list[DemandResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_demands(db)


@router.get(
    "/{demand_id}",
    response_model=DemandResponse
)
def get_one(
    demand_id: int,
    db: Session = Depends(get_db)
):
    demand = get_demand(db, demand_id)

    if demand is None:
        raise HTTPException(
            status_code=404,
            detail="Demand record not found"
        )

    return demand


@router.delete("/{demand_id}")
def delete(
    demand_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_demand(
        db,
        demand_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Demand record not found"
        )

    return {
        "message": "Demand record deleted successfully"
    }