from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryAnalysisResponse,
    InventoryForecastAnalysisResponse
)

from app.services.inventory_service import (
    create_inventory,
    get_inventories,
    get_inventory,
    update_inventory,
    delete_inventory,
    analyze_inventory,
    analyze_inventory_with_forecast
)


router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)


@router.post(
    "",
    response_model=InventoryResponse,
    status_code=201
)
def create(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_inventory(
            db,
            inventory_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get(
    "",
    response_model=list[InventoryResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_inventories(db)


@router.get(
    "/forecast-analysis/{product_id}/{warehouse_id}",
    response_model=InventoryForecastAnalysisResponse
)
def analyze_with_forecast(
    product_id: int,
    warehouse_id: int,
    window: int = 3,
    db: Session = Depends(get_db)
):
    try:
        return analyze_inventory_with_forecast(
            db=db,
            product_id=product_id,
            warehouse_id=warehouse_id,
            window=window
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse
)
def get_one(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory = get_inventory(
        db,
        inventory_id
    )

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )

    return inventory


@router.put(
    "/{inventory_id}",
    response_model=InventoryResponse
)
def update(
    inventory_id: int,
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db)
):
    try:
        inventory = update_inventory(
            db,
            inventory_id,
            inventory_data
        )

        if inventory is None:
            raise HTTPException(
                status_code=404,
                detail="Inventory record not found"
            )

        return inventory

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.delete("/{inventory_id}")
def delete(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_inventory(
        db,
        inventory_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )

    return {
        "message": "Inventory record deleted successfully"
    }


@router.get(
    "/analysis/{product_id}/{warehouse_id}",
    response_model=InventoryAnalysisResponse
)
def analyze(
    product_id: int,
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    try:
        return analyze_inventory(
            db,
            product_id,
            warehouse_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )