from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate


def create_vehicle(
    db: Session,
    vehicle_data: VehicleCreate
):
    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_number == vehicle_data.vehicle_number
    ).first()

    if existing_vehicle is not None:
        raise ValueError(
            "Vehicle with this vehicle number already exists"
        )

    if vehicle_data.capacity <= 0:
        raise ValueError(
            "Vehicle capacity must be positive"
        )

    if vehicle_data.fixed_cost < 0:
        raise ValueError(
            "Fixed cost cannot be negative"
        )

    if vehicle_data.cost_per_km < 0:
        raise ValueError(
            "Cost per km cannot be negative"
        )

    vehicle = Vehicle(
        vehicle_number=vehicle_data.vehicle_number,
        capacity=vehicle_data.capacity,
        fixed_cost=vehicle_data.fixed_cost,
        cost_per_km=vehicle_data.cost_per_km
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


def get_vehicles(db: Session):
    return db.query(Vehicle).all()


def get_vehicle(
    db: Session,
    vehicle_id: int
):
    return db.query(Vehicle).filter(
        Vehicle.vehicle_id == vehicle_id
    ).first()


def update_vehicle(
    db: Session,
    vehicle_id: int,
    vehicle_data: VehicleCreate
):
    vehicle = get_vehicle(db, vehicle_id)

    if vehicle is None:
        return None

    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_number == vehicle_data.vehicle_number,
        Vehicle.vehicle_id != vehicle_id
    ).first()

    if existing_vehicle is not None:
        raise ValueError(
            "Vehicle with this vehicle number already exists"
        )

    if vehicle_data.capacity <= 0:
        raise ValueError(
            "Vehicle capacity must be positive"
        )

    if vehicle_data.fixed_cost < 0:
        raise ValueError(
            "Fixed cost cannot be negative"
        )

    if vehicle_data.cost_per_km < 0:
        raise ValueError(
            "Cost per km cannot be negative"
        )

    vehicle.vehicle_number = vehicle_data.vehicle_number
    vehicle.capacity = vehicle_data.capacity
    vehicle.fixed_cost = vehicle_data.fixed_cost
    vehicle.cost_per_km = vehicle_data.cost_per_km

    db.commit()
    db.refresh(vehicle)

    return vehicle


def delete_vehicle(
    db: Session,
    vehicle_id: int
):
    vehicle = get_vehicle(db, vehicle_id)

    if vehicle is None:
        return False

    db.delete(vehicle)
    db.commit()

    return True