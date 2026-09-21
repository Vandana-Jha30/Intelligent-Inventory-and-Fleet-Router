import time

from app.optimization.vehicle_routing_optimizer import (
    solve_vehicle_routing
)
from app.optimization.vehicle_routing_solver import (
    solve_vehicle_routing_optimized
)


def _calculate_metrics(result, vehicles):
    """
    Calculate common metrics from a routing solution.
    """

    routes = result["routes"]

    used_routes = [
        route
        for route in routes
        if route["location_ids"]
    ]

    total_capacity = sum(
        vehicle.capacity
        for vehicle in vehicles
        if vehicle.vehicle_id in {
            route["vehicle_id"]
            for route in used_routes
        }
    )

    total_demand = sum(
        route["total_demand"]
        for route in used_routes
    )

    if total_capacity > 0:
        capacity_utilization = (
            total_demand / total_capacity
        )
    else:
        capacity_utilization = 0.0

    return {
        "vehicles_used": len(used_routes),
        "total_distance": result["total_distance"],
        "total_cost": result["total_cost"],
        "capacity_utilization": capacity_utilization
    }


def compare_vehicle_routing(
    depot,
    delivery_locations,
    vehicles
):
    """
    Compare the First-Fit Decreasing heuristic
    against the OR-Tools CVRP solution using
    the same input data.
    """

    # ---------------------------------
    # Run heuristic
    # ---------------------------------

    heuristic_start = time.perf_counter()

    heuristic_result = solve_vehicle_routing(
        depot=depot,
        delivery_locations=delivery_locations,
        vehicles=vehicles
    )

    heuristic_time = (
        time.perf_counter() - heuristic_start
    ) * 1000

    # ---------------------------------
    # Run OR-Tools
    # ---------------------------------

    ortools_start = time.perf_counter()

    ortools_result = solve_vehicle_routing_optimized(
        depot=depot,
        delivery_locations=delivery_locations,
        vehicles=vehicles
    )

    ortools_time = (
        time.perf_counter() - ortools_start
    ) * 1000

    # ---------------------------------
    # Common metrics
    # ---------------------------------

    heuristic_metrics = _calculate_metrics(
        heuristic_result,
        vehicles
    )

    ortools_metrics = _calculate_metrics(
        ortools_result,
        vehicles
    )

    heuristic_metrics["execution_time_ms"] = (
        heuristic_time
    )

    ortools_metrics["execution_time_ms"] = (
        ortools_time
    )

    # ---------------------------------
    # Differences
    # ---------------------------------

    distance_difference = (
        heuristic_metrics["total_distance"]
        - ortools_metrics["total_distance"]
    )

    cost_difference = (
        heuristic_metrics["total_cost"]
        - ortools_metrics["total_cost"]
    )

    if heuristic_metrics["total_cost"] != 0:
        cost_difference_percent = (
            cost_difference
            / heuristic_metrics["total_cost"]
        ) * 100
    else:
        cost_difference_percent = 0.0

    return {
        "heuristic": {
            **heuristic_metrics,
            "routes": heuristic_result["routes"]
        },
        "ortools": {
            **ortools_metrics,
            "routes": ortools_result["routes"]
        },
        "comparison": {
            "distance_difference": distance_difference,
            "cost_difference": cost_difference,
            "cost_difference_percent": (
                cost_difference_percent
            )
        }
    }