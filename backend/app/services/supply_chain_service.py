from sqlalchemy.orm import Session

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle

from app.services.inventory_service import analyze_inventory_with_forecast
from app.optimization.vehicle_routing_solver import solve_vehicle_routing_optimized


def create_supply_chain_plan(
    db: Session,
    product_id: int,
    warehouse_id: int,
    depot_id: int,
    delivery_location_ids=None,
    window: int = 3,
):
    """Create an integrated inventory and distribution plan.

    Inventory replenishment and customer distribution are deliberately kept
    as separate decisions:

    1. Inventory analysis determines whether the warehouse needs replenishment
       and, if so, the recommended order quantity.
    2. Customer delivery demand comes from delivery-location records and is
       routed independently using the CVRP solver.

    The planner therefore does not incorrectly require customer demand to be
    less than or equal to a supplier replenishment order. Existing inventory
    can satisfy customer deliveries even when no new replenishment is needed.
    """

    inventory_analysis = analyze_inventory_with_forecast(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        window=window,
    )

    depot = db.query(Depot).filter(
        Depot.depot_id == depot_id
    ).first()

    if depot is None:
        raise ValueError("Depot not found")

    query = db.query(DeliveryLocation)

    if delivery_location_ids is not None:
        if len(delivery_location_ids) != len(set(delivery_location_ids)):
            raise ValueError(
                "Each delivery location can appear only once"
            )

        locations = query.filter(
            DeliveryLocation.location_id.in_(delivery_location_ids)
        ).all()

        locations_by_id = {
            location.location_id: location
            for location in locations
        }

        missing_ids = [
            location_id
            for location_id in delivery_location_ids
            if location_id not in locations_by_id
        ]

        if missing_ids:
            raise ValueError(
                f"Delivery location not found: {missing_ids[0]}"
            )

        # Preserve the order requested by the caller.
        locations = [
            locations_by_id[location_id]
            for location_id in delivery_location_ids
        ]
    else:
        locations = query.order_by(
            DeliveryLocation.location_id
        ).all()

    if not locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    vehicles = db.query(Vehicle).all()

    if not vehicles:
        raise ValueError("At least one vehicle is required")

    delivery_demand = sum(
        float(location.demand_quantity)
        for location in locations
    )

    routing = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles,
    )

    return {
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "depot_id": depot_id,
        "delivery_demand": delivery_demand,
        "inventory_analysis": inventory_analysis,
        "routing": routing,
    }
