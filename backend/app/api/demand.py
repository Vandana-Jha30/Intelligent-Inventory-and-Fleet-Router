from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.demand import (
    DemandCreate,
    DemandResponse,
    DemandForecastResponse
)

from app.services.demand_service import (
    create_demand,
    get_demands,
    get_demand,
    delete_demand
)

from app.optimization.demand_forecaster import (
    moving_average_forecast
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


@router.get(
    "/forecast/{product_id}/{warehouse_id}",
    response_model=DemandForecastResponse
)
def forecast(
    product_id: int,
    warehouse_id: int,
    window: int = 3,
    db: Session = Depends(get_db)
):
    demands = get_demands(db)

    filtered_demands = [
        demand.quantity
        for demand in demands
        if demand.product_id == product_id
        and demand.warehouse_id == warehouse_id
    ]

    try:
        forecast_value = moving_average_forecast(
            filtered_demands,
            window
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "method": "moving_average",
        "window": window,
        "forecast": forecast_value
    }


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

