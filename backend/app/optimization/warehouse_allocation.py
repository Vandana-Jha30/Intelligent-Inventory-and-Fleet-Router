from app.optimization.distance_calculator import calculate_distance


def _calculate_warehouse_location_distance(warehouse, location):
    return calculate_distance(
        warehouse.latitude,
        warehouse.longitude,
        location.latitude,
        location.longitude,
    )


def nearest_warehouse_allocation(
    warehouses,
    inventory_by_warehouse,
    delivery_locations,
    distance_function=_calculate_warehouse_location_distance,
):
    """
    Create a baseline warehouse allocation using a nearest-warehouse rule.

    Each customer is served by the nearest warehouse with available
    inventory. If the nearest warehouse cannot satisfy the complete
    demand, the remaining demand is assigned to the next-nearest
    warehouse.
    """
    remaining_inventory = {
        warehouse_id: float(quantity)
        for warehouse_id, quantity in inventory_by_warehouse.items()
    }

    allocation = []
    total_cost = 0.0
    total_flow = 0.0

    for location in delivery_locations:
        remaining_demand = float(location.demand_quantity)

        candidate_warehouses = []

        for warehouse in warehouses:
            available = remaining_inventory.get(
                warehouse.warehouse_id,
                0.0,
            )

            if available <= 0:
                continue

            distance = distance_function(
                warehouse,
                location,
            )

            candidate_warehouses.append(
                (distance, warehouse)
            )

        candidate_warehouses.sort(
            key=lambda item: item[0]
        )

        for distance, warehouse in candidate_warehouses:
            if remaining_demand <= 0:
                break

            available = remaining_inventory[
                warehouse.warehouse_id
            ]

            quantity = min(
                available,
                remaining_demand,
            )

            if quantity <= 0:
                continue

            transportation_cost = quantity * distance

            allocation.append(
                {
                    "warehouse_id": warehouse.warehouse_id,
                    "warehouse_name": warehouse.name,
                    "location_id": location.location_id,
                    "location_name": location.location_name,
                    "quantity": quantity,
                    "distance_km": distance,
                    "transportation_cost": transportation_cost,
                }
            )

            remaining_inventory[
                warehouse.warehouse_id
            ] -= quantity

            remaining_demand -= quantity
            total_flow += quantity
            total_cost += transportation_cost

        if remaining_demand > 1e-9:
            raise ValueError(
                "Insufficient available inventory to satisfy delivery demand"
            )

    return {
        "total_cost": total_cost,
        "total_flow": total_flow,
        "allocation": allocation,
    }