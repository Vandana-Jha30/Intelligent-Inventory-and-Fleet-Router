from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.supply_chain import (
    SupplyChainPlanRequest,
    SupplyChainPlanResponse,
)
from app.services.supply_chain_service import create_supply_chain_plan


router = APIRouter(
    prefix="/api/supply-chain",
    tags=["Supply Chain Planning"],
)


@router.post(
    "/plan",
    response_model=SupplyChainPlanResponse,
)
def plan(
    request: SupplyChainPlanRequest,
    db: Session = Depends(get_db),
):
    try:
        return create_supply_chain_plan(
            db=db,
            product_id=request.product_id,
            warehouse_id=request.warehouse_id,
            depot_id=request.depot_id,
            delivery_location_ids=request.delivery_location_ids,
            window=request.window,
        )
    except ValueError as error:
        message = str(error)

        if message in {
            "Product not found",
            "Warehouse not found",
            "Inventory record not found",
            "Depot not found",
        } or message.startswith("Delivery location not found"):
            raise HTTPException(status_code=404, detail=message)

        raise HTTPException(status_code=400, detail=message)

