from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseResponse
)
from app.services.warehouse_service import (
    create_warehouse,
    get_warehouses,
    get_warehouse,
    update_warehouse,
    delete_warehouse
)


router = APIRouter(
    prefix="/api/warehouses",
    tags=["Warehouses"]
)


@router.post(
    "",
    response_model=WarehouseResponse
)
def create(
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db)
):
    return create_warehouse(db, warehouse_data)


@router.get(
    "",
    response_model=list[WarehouseResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_warehouses(db)


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def get_one(
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    warehouse = get_warehouse(db, warehouse_id)

    if warehouse is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    return warehouse


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def update(
    warehouse_id: int,
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db)
):
    warehouse = update_warehouse(
        db,
        warehouse_id,
        warehouse_data
    )

    if warehouse is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    return warehouse


@router.delete("/{warehouse_id}")
def delete(
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_warehouse(
        db,
        warehouse_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    return {
        "message": "Warehouse deleted successfully"
    }