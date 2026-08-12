from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(
    db: Session,
    product_data: ProductCreate
):
    product = Product(
        sku=product_data.sku,
        name=product_data.name,
        unit_cost=product_data.unit_cost,
        ordering_cost=product_data.ordering_cost,
        holding_cost=product_data.holding_cost,
        lead_time_days=product_data.lead_time_days,
        service_level=product_data.service_level
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(Product).all()


def get_product(
    db: Session,
    product_id: int
):
    return db.query(Product).filter(
        Product.product_id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductCreate
):
    product = get_product(db, product_id)

    if product is None:
        return None

    product.sku = product_data.sku
    product.name = product_data.name
    product.unit_cost = product_data.unit_cost
    product.ordering_cost = product_data.ordering_cost
    product.holding_cost = product_data.holding_cost
    product.lead_time_days = product_data.lead_time_days
    product.service_level = product_data.service_level

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):
    product = get_product(db, product_id)

    if product is None:
        return False

    db.delete(product)
    db.commit()

    return True