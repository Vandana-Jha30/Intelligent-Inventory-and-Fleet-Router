from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate


def create_warehouse(
    db: Session,
    warehouse_data: WarehouseCreate
):
    warehouse = Warehouse(
        name=warehouse_data.name,
        latitude=warehouse_data.latitude,
        longitude=warehouse_data.longitude,
        capacity=warehouse_data.capacity,
        operating_cost=warehouse_data.operating_cost
    )

    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)

    return warehouse


def get_warehouses(db: Session):
    return db.query(Warehouse).all()


def get_warehouse(
    db: Session,
    warehouse_id: int
):
    return db.query(Warehouse).filter(
        Warehouse.warehouse_id == warehouse_id
    ).first()


def update_warehouse(
    db: Session,
    warehouse_id: int,
    warehouse_data: WarehouseCreate
):
    warehouse = get_warehouse(db, warehouse_id)

    if warehouse is None:
        return None

    warehouse.name = warehouse_data.name
    warehouse.latitude = warehouse_data.latitude
    warehouse.longitude = warehouse_data.longitude
    warehouse.capacity = warehouse_data.capacity
    warehouse.operating_cost = warehouse_data.operating_cost

    db.commit()
    db.refresh(warehouse)

    return warehouse


def delete_warehouse(
    db: Session,
    warehouse_id: int
):
    warehouse = get_warehouse(db, warehouse_id)

    if warehouse is None:
        return False

    db.delete(warehouse)
    db.commit()

    return True