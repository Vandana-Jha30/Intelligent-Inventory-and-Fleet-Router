from sqlalchemy.orm import Session

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle

from app.optimization.vehicle_routing_solver import (
    solve_vehicle_routing_optimized
)

from app.optimization.routing_comparison import (
    compare_vehicle_routing
)

def solve_routing(
    db: Session,
    depot_id: int
):
    # Get depot

    depot = db.query(Depot).filter(
        Depot.depot_id == depot_id
    ).first()

    if depot is None:
        raise ValueError(
            "Depot not found"
        )

    # Get all delivery locations

    delivery_locations = (
        db.query(DeliveryLocation)
        .all()
    )

    if not delivery_locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    # Get all vehicles

    vehicles = (
        db.query(Vehicle)
        .all()
    )

    if not vehicles:
        raise ValueError(
            "At least one vehicle is required"
        )

    # Run OR-Tools CVRP solver

    result = solve_vehicle_routing_optimized(
        depot,
        delivery_locations,
        vehicles
    )

    return result



def compare_routing(
    db: Session,
    depot_id: int
):
    # Get depot

    depot = db.query(Depot).filter(
        Depot.depot_id == depot_id
    ).first()

    if depot is None:
        raise ValueError(
            "Depot not found"
        )

    # Get all delivery locations

    delivery_locations = (
        db.query(DeliveryLocation)
        .all()
    )

    if not delivery_locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    # Get all vehicles

    vehicles = (
        db.query(Vehicle)
        .all()
    )

    if not vehicles:
        raise ValueError(
            "At least one vehicle is required"
        )

    # Run heuristic vs OR-Tools comparison

    result = compare_vehicle_routing(
        depot=depot,
        delivery_locations=delivery_locations,
        vehicles=vehicles
    )

    return result