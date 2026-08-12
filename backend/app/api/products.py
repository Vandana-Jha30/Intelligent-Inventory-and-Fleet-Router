from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse
)
def create(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product_data)


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_one(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = update_product(
        db,
        product_id,
        product_data
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.delete("/{product_id}")
def delete(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_product(
        db,
        product_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }