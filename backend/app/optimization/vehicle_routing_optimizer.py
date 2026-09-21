from app.optimization.distance_calculator import (
    calculate_distance
)


def solve_vehicle_routing(
    depot,
    delivery_locations,
    vehicles
):
    # -----------------------------
    # Input validation
    # -----------------------------

    if depot is None:
        raise ValueError("Depot is required")

    if not delivery_locations:
        raise ValueError(
            "At least one delivery location is required"
        )

    if not vehicles:
        raise ValueError(
            "At least one vehicle is required"
        )

    # -----------------------------
    # Capacity feasibility checks
    # -----------------------------

    total_demand = sum(
        location.demand_quantity
        for location in delivery_locations
    )

    total_vehicle_capacity = sum(
        vehicle.capacity
        for vehicle in vehicles
    )

    if total_demand > total_vehicle_capacity:
        raise ValueError(
            "Total vehicle capacity is insufficient"
        )

    max_vehicle_capacity = max(
        vehicle.capacity
        for vehicle in vehicles
    )

    # A delivery cannot be split between vehicles
    # in the current version.
    for location in delivery_locations:
        if location.demand_quantity > max_vehicle_capacity:
            raise ValueError(
                "A delivery location demand exceeds vehicle capacity"
            )

    # -----------------------------
    # Create vehicle routes
    # -----------------------------

    routes = []

    # Larger vehicles are considered first
    sorted_vehicles = sorted(
        vehicles,
        key=lambda vehicle: vehicle.capacity,
        reverse=True
    )

    for vehicle in sorted_vehicles:
        routes.append({
            "vehicle_id": vehicle.vehicle_id,
            "location_ids": [],
            "total_demand": 0.0,
            "remaining_capacity": vehicle.capacity,
            "route_distance": 0.0,
            "route_cost": 0.0
        })

    # -----------------------------
    # Assign delivery locations
    # -----------------------------

    # Larger-demand locations are assigned first.
    # This is a First-Fit Decreasing style
    # capacity assignment heuristic.
    sorted_locations = sorted(
        delivery_locations,
        key=lambda location: location.demand_quantity,
        reverse=True
    )

    for location in sorted_locations:
        assigned = False

        for route in routes:
            if route["remaining_capacity"] >= location.demand_quantity:

                route["location_ids"].append(
                    location.location_id
                )

                route["total_demand"] += (
                    location.demand_quantity
                )

                route["remaining_capacity"] -= (
                    location.demand_quantity
                )

                assigned = True
                break

        if not assigned:
            raise ValueError(
                "Unable to assign delivery location to a vehicle"
            )

    # -----------------------------
    # Calculate route distances
    # -----------------------------
    #
    # Each route follows:
    #
    # Depot
    #   ↓
    # Location A
    #   ↓
    # Location B
    #   ↓
    # Location C
    #   ↓
    # Depot
    #
    # The current location order is the same
    # order in which locations were assigned.
    # Route-order optimization will be added later.
    # -----------------------------

    for route in routes:

        current_latitude = depot.latitude
        current_longitude = depot.longitude

        for location_id in route["location_ids"]:

            location = next(
                location
                for location in delivery_locations
                if location.location_id == location_id
            )

            distance = calculate_distance(
                current_latitude,
                current_longitude,
                location.latitude,
                location.longitude
            )

            route["route_distance"] += distance

            # Move current position to this delivery location
            current_latitude = location.latitude
            current_longitude = location.longitude

        # Return from the last delivery location
        # back to the depot
        return_distance = calculate_distance(
            current_latitude,
            current_longitude,
            depot.latitude,
            depot.longitude
        )

        route["route_distance"] += return_distance

    # -----------------------------
    # Calculate total fleet distance
    # -----------------------------

    total_distance = sum(
        route["route_distance"]
        for route in routes
    )

    # -----------------------------
    # Calculate route costs
    # -----------------------------

    for route in routes:

        # Find the vehicle associated with this route
        vehicle = next(
            vehicle
            for vehicle in vehicles
            if vehicle.vehicle_id == route["vehicle_id"]
        )

        # Fixed cost is charged only when
        # the vehicle is actually used.
        if route["location_ids"]:
            route["route_cost"] = (
                vehicle.fixed_cost
                + (
                    vehicle.cost_per_km
                    * route["route_distance"]
                )
            )
        else:
            route["route_cost"] = 0.0

    # -----------------------------
    # Calculate total fleet cost
    # -----------------------------

    total_cost = sum(
        route["route_cost"]
        for route in routes
    )

    # -----------------------------
    # Final result
    # -----------------------------

    return {
        "total_distance": total_distance,
        "total_cost": total_cost,
        "routes": routes
    }