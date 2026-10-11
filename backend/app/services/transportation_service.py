from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.models.delivery_location import DeliveryLocation

from app.optimization.transportation_solver import (
    solve_transportation
)


def solve_transportation_plan(
    db: Session,
    warehouse_ids=None,
    delivery_location_ids=None
):
    """
    Create an optimized warehouse-to-customer
    transportation plan.

    The transportation solver determines:
        - how much each warehouse should ship
        - which warehouse supplies each customer
        - transportation distance/cost
        - remaining warehouse supply

    Vehicle routing is handled separately.
    """

    # ---------------------------------
    # Get warehouses
    # ---------------------------------

    warehouse_query = db.query(Warehouse)

    if warehouse_ids is not None:

        if len(warehouse_ids) != len(set(warehouse_ids)):
            raise ValueError(
                "Each warehouse can appear only once"
            )

        warehouses = warehouse_query.filter(
            Warehouse.warehouse_id.in_(warehouse_ids)
        ).all()

        warehouses_by_id = {
            warehouse.warehouse_id: warehouse
            for warehouse in warehouses
        }

        missing_ids = [
            warehouse_id
            for warehouse_id in warehouse_ids
            if warehouse_id not in warehouses_by_id
        ]

        if missing_ids:
            raise ValueError(
                f"Warehouse not found: {missing_ids[0]}"
            )

        # Preserve caller order.
        warehouses = [
            warehouses_by_id[warehouse_id]
            for warehouse_id in warehouse_ids
        ]

    else:

        warehouses = warehouse_query.order_by(
            Warehouse.warehouse_id
        ).all()

    if not warehouses:
        raise ValueError(
            "At least one warehouse is required"
        )

    # ---------------------------------
    # Get delivery locations
    # ---------------------------------

    location_query = db.query(
        DeliveryLocation
    )

    if delivery_location_ids is not None:

        if (
            len(delivery_location_ids)
            != len(set(delivery_location_ids))
        ):
            raise ValueError(
                "Each delivery location can appear only once"
            )

        locations = location_query.filter(
            DeliveryLocation.location_id.in_(
                delivery_location_ids
            )
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

        # Preserve caller order.
        locations = [
            locations_by_id[location_id]
            for location_id in delivery_location_ids
        ]

    else:

        locations = location_query.order_by(
            DeliveryLocation.location_id
        ).all()

    if not locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    # ---------------------------------
    # Solve transportation problem
    # ---------------------------------

    result = solve_transportation(
        warehouses,
        locations
    )

    return result