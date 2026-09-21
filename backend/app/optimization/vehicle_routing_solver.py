from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

QUANTITY_SCALE = 100


def solve_vehicle_routing_optimized(
    depot,
    delivery_locations,
    vehicles,
    time_limit_seconds=5
):
    """
    Solve the Capacitated Vehicle Routing Problem (CVRP)
    using Google OR-Tools.

    Objective:
        Minimize total fleet cost consisting of:
        1. Fixed cost for every used vehicle
        2. Distance-based travel cost

    Each delivery location must be visited exactly once.
    Each vehicle starts and ends at the depot.
    Vehicle capacity constraints are enforced.
    """

    # Input validation

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

    # ---------------------------------
    # Capacity feasibility
    # ---------------------------------

    total_demand = sum(
        location.demand_quantity
        for location in delivery_locations
    )

    total_capacity = sum(
        vehicle.capacity
        for vehicle in vehicles
    )

    max_vehicle_capacity = max(
        vehicle.capacity
        for vehicle in vehicles
    )

    # Check individual delivery feasibility first.
    # A delivery cannot be split between vehicles
    # in the current model.
    for location in delivery_locations:

        if location.demand_quantity > max_vehicle_capacity:
            raise ValueError(
                "A delivery location demand exceeds vehicle capacity"
            )

    # Then check whether the total fleet capacity
    # is sufficient for all deliveries.
    if total_demand > total_capacity:
        raise ValueError(
            "Total vehicle capacity is insufficient"
        )

    # ---------------------------------
    # Create node list
    #
    # Index 0 = depot
    # Index 1...n = delivery locations
    # ---------------------------------

    locations = [depot] + list(delivery_locations)

    number_of_locations = len(locations)
    number_of_vehicles = len(vehicles)

    depot_index = 0

    # Create distance matrix

    from app.optimization.distance_calculator import (
        calculate_distance
    )

    distance_matrix = []

    for i in range(number_of_locations):

        row = []

        for j in range(number_of_locations):

            distance = calculate_distance(
                locations[i].latitude,
                locations[i].longitude,
                locations[j].latitude,
                locations[j].longitude
            )

            row.append(distance)

        distance_matrix.append(row)

    # OR-Tools routing manager

    manager = pywrapcp.RoutingIndexManager(
        number_of_locations,
        number_of_vehicles,
        depot_index
    )

    routing = pywrapcp.RoutingModel(manager)

    # ---------------------------------
    # Vehicle fixed costs
    # ---------------------------------

    for vehicle_index, vehicle in enumerate(vehicles):
        routing.SetFixedCostOfVehicle(
            int(round(vehicle.fixed_cost * 1000)),
            vehicle_index
        )


    # Distance callback

    def distance_callback(from_index, to_index):

        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        return int(
            round(
                distance_matrix[from_node][to_node] * 1000
            )
        )


    # ---------------------------------
    # Vehicle-specific travel costs
    #
    # OR-Tools routing models use integer
    # arc costs, so we scale monetary cost
    # to preserve decimal precision.
    # ---------------------------------

    for vehicle_index, vehicle in enumerate(vehicles):

        def cost_callback(
            from_index,
            to_index,
            vehicle=vehicle
        ):

            from_node = manager.IndexToNode(
                from_index
            )

            to_node = manager.IndexToNode(
                to_index
            )

            distance = distance_matrix[
                from_node
            ][to_node]

            travel_cost = (
                distance * vehicle.cost_per_km
            )

            return int(
                round(
                    travel_cost * 1000
                )
            )

        cost_callback_index = (
            routing.RegisterTransitCallback(
                cost_callback
            )
        )

        routing.SetArcCostEvaluatorOfVehicle(
            cost_callback_index,
            vehicle_index
        )


    # Capacity constraint

    demands = [0]

    demands.extend(
        int(round(location.demand_quantity * QUANTITY_SCALE))
        for location in delivery_locations
    )

    def demand_callback(from_index):

        from_node = manager.IndexToNode(
            from_index
        )

        return demands[from_node]

    demand_callback_index = (
        routing.RegisterUnaryTransitCallback(
            demand_callback
        )
    )

    vehicle_capacities = [
        int(round(vehicle.capacity * QUANTITY_SCALE))
        for vehicle in vehicles
    ]

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        vehicle_capacities,
        True,
        "Capacity"
    )

    # ---------------------------------
    # Allow unused vehicles

    # A vehicle that serves no locations
    # does not incur a fixed cost in the
    # final result.
    # ---------------------------------


    # Search parameters

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    # Limit solver runtime.
    search_parameters.time_limit.seconds = (time_limit_seconds)


    # Solve

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        raise ValueError(
            "No feasible routing solution found"
        )


    # Extract routes

    routes = []

    total_distance = 0.0
    total_cost = 0.0

    for vehicle_index, vehicle in enumerate(vehicles):

        index = routing.Start(vehicle_index)

        route_location_ids = []
        route_distance = 0.0

        while not routing.IsEnd(index):

            node_index = manager.IndexToNode(index)

            if node_index != depot_index:

                location = locations[node_index]

                route_location_ids.append(
                    location.location_id
                )

            previous_index = index

            index = solution.Value(
                routing.NextVar(index)
            )

            from_node = manager.IndexToNode(
                previous_index
            )

            to_node = manager.IndexToNode(
                index
            )

            route_distance += distance_matrix[
                from_node
            ][to_node]


        # Calculate route cost

        if route_location_ids:

            route_cost = (
                vehicle.fixed_cost
                + (
                    vehicle.cost_per_km
                    * route_distance
                )
            )

        else:

            route_cost = 0.0

        route = {
            "vehicle_id": vehicle.vehicle_id,
            "location_ids": route_location_ids,
            "total_demand": sum(
                location.demand_quantity
                for location in delivery_locations
                if location.location_id
                in route_location_ids
            ),
            "remaining_capacity": (
                vehicle.capacity
                - sum(
                    location.demand_quantity
                    for location in delivery_locations
                    if location.location_id
                    in route_location_ids
                )
            ),
            "route_distance": route_distance,
            "route_cost": route_cost
        }

        routes.append(route)

        total_distance += route_distance
        total_cost += route_cost


    # Final result

    return {
        "total_distance": total_distance,
        "total_cost": total_cost,
        "routes": routes
    }