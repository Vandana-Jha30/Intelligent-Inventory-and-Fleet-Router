from sqlalchemy.orm import Session

from app.models.depot import Depot
from app.schemas.depot import DepotCreate


def create_depot(
    db: Session,
    depot_data: DepotCreate
):
    depot = Depot(
        depot_name=depot_data.depot_name,
        latitude=depot_data.latitude,
        longitude=depot_data.longitude
    )

    db.add(depot)
    db.commit()
    db.refresh(depot)

    return depot


def get_depots(db: Session):
    return db.query(Depot).all()


def get_depot(
    db: Session,
    depot_id: int
):
    return db.query(Depot).filter(
        Depot.depot_id == depot_id
    ).first()


def update_depot(
    db: Session,
    depot_id: int,
    depot_data: DepotCreate
):
    depot = get_depot(
        db,
        depot_id
    )

    if depot is None:
        return None

    depot.depot_name = depot_data.depot_name
    depot.latitude = depot_data.latitude
    depot.longitude = depot_data.longitude

    db.commit()
    db.refresh(depot)

    return depot


def delete_depot(
    db: Session,
    depot_id: int
):
    depot = get_depot(
        db,
        depot_id
    )

    if depot is None:
        return False

    db.delete(depot)
    db.commit()

    return True