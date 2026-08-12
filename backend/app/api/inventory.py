from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.inventory import InventoryAnalysisResponse
from app.services.inventory_service import analyze_inventory


router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)


@router.get(
    "/analyze/{product_id}/{warehouse_id}",
    response_model=InventoryAnalysisResponse
)
def analyze(
    product_id: int,
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = analyze_inventory(
            db,
            product_id,
            warehouse_id
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )