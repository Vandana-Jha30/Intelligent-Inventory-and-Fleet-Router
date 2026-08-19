from sqlalchemy.orm import Session

from app.models.delivery_location import DeliveryLocation
from app.schemas.delivery_location import DeliveryLocationCreate


def create_delivery_location(
    db: Session,
    location_data: DeliveryLocationCreate
):
    location = DeliveryLocation(
        location_name=location_data.location_name,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        demand_quantity=location_data.demand_quantity
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def get_delivery_locations(db: Session):
    return db.query(DeliveryLocation).all()


def get_delivery_location(
    db: Session,
    location_id: int
):
    return db.query(DeliveryLocation).filter(
        DeliveryLocation.location_id == location_id
    ).first()


def update_delivery_location(
    db: Session,
    location_id: int,
    location_data: DeliveryLocationCreate
):
    location = get_delivery_location(
        db,
        location_id
    )

    if location is None:
        return None

    location.location_name = location_data.location_name
    location.latitude = location_data.latitude
    location.longitude = location_data.longitude
    location.demand_quantity = location_data.demand_quantity

    db.commit()
    db.refresh(location)

    return location


def delete_delivery_location(
    db: Session,
    location_id: int
):
    location = get_delivery_location(
        db,
        location_id
    )

    if location is None:
        return False

    db.delete(location)
    db.commit()

    return True