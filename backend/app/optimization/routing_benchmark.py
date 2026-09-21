import random
import time

from types import SimpleNamespace

from app.optimization.vehicle_routing_optimizer import (
    solve_vehicle_routing
)

from app.optimization.vehicle_routing_solver import (
    solve_vehicle_routing_optimized
)


def generate_benchmark_data(
    number_of_locations,
    number_of_vehicles,
    seed=42
):
    """
    Generate a deterministic synthetic vehicle-routing
    scenario for benchmarking.

    The same seed produces the same scenario.
    """

    random.seed(seed)

    # Fixed depot around Bengaluru coordinates
    depot = SimpleNamespace(
        depot_id=1,
        depot_name="Benchmark Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    # Generate customer locations around the depot
    delivery_locations = []

    for location_id in range(
        1,
        number_of_locations + 1
    ):

        latitude = (
            12.9716
            + random.uniform(-0.05, 0.05)
        )

        longitude = (
            77.5946
            + random.uniform(-0.05, 0.05)
        )

        demand = random.randint(10, 50)

        delivery_locations.append(
            SimpleNamespace(
                location_id=location_id,
                location_name=(
                    f"Customer {location_id}"
                ),
                latitude=latitude,
                longitude=longitude,
                demand_quantity=demand
            )
        )

    # Generate vehicles
    #
    # Each vehicle has capacity 100.
    #
    # Total fleet capacity is deliberately
    # larger than expected total demand.

    vehicles = []

    for vehicle_id in range(
        1,
        number_of_vehicles + 1
    ):

        vehicles.append(
            SimpleNamespace(
                vehicle_id=vehicle_id,
                vehicle_number=(
                    f"BENCH-TRUCK-{vehicle_id:03d}"
                ),
                capacity=100,
                fixed_cost=500,
                cost_per_km=20
            )
        )

    return (
        depot,
        delivery_locations,
        vehicles
    )


def _calculate_metrics(
    result,
    execution_time_ms
):
    """
    Extract common benchmark metrics.
    """

    routes = result["routes"]

    used_routes = [
        route
        for route in routes
        if route["location_ids"]
    ]

    total_demand = sum(
        route["total_demand"]
        for route in used_routes
    )

    total_capacity = sum(
        route["total_demand"]
        + route["remaining_capacity"]
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
        "capacity_utilization": (
            capacity_utilization
        ),
        "execution_time_ms": execution_time_ms
    }


def benchmark_routing_scenario(
    depot,
    delivery_locations,
    vehicles,
    time_limit_seconds=1
):
    """
    Benchmark the FFD heuristic against OR-Tools
    using exactly the same routing scenario.
    """

    # ---------------------------------
    # Heuristic
    # ---------------------------------

    heuristic_start = time.perf_counter()

    heuristic_result = solve_vehicle_routing(
        depot=depot,
        delivery_locations=delivery_locations,
        vehicles=vehicles
    )

    heuristic_time = (
        time.perf_counter()
        - heuristic_start
    ) * 1000

    # ---------------------------------
    # OR-Tools
    # ---------------------------------

    ortools_start = time.perf_counter()

    ortools_result = (
        solve_vehicle_routing_optimized(
            depot=depot,
            delivery_locations=delivery_locations,
            vehicles=vehicles,
            time_limit_seconds=(
                time_limit_seconds
            )
        )
    )

    ortools_time = (
        time.perf_counter()
        - ortools_start
    ) * 1000

    # ---------------------------------
    # Metrics
    # ---------------------------------

    heuristic_metrics = _calculate_metrics(
        heuristic_result,
        heuristic_time
    )

    ortools_metrics = _calculate_metrics(
        ortools_result,
        ortools_time
    )

    # ---------------------------------
    # Comparison
    # ---------------------------------

    cost_difference = (
        heuristic_metrics["total_cost"]
        - ortools_metrics["total_cost"]
    )

    distance_difference = (
        heuristic_metrics["total_distance"]
        - ortools_metrics["total_distance"]
    )

    if heuristic_metrics["total_cost"] != 0:

        cost_difference_percent = (
            cost_difference
            / heuristic_metrics["total_cost"]
        ) * 100

    else:

        cost_difference_percent = 0.0

    return {
        "heuristic": heuristic_metrics,
        "ortools": ortools_metrics,
        "comparison": {
            "distance_difference": (
                distance_difference
            ),
            "cost_difference": (
                cost_difference
            ),
            "cost_difference_percent": (
                cost_difference_percent
            )
        }
    }


def run_routing_benchmark(
    scenarios=None,
    time_limit_seconds=1
):
    """
    Run multiple routing benchmark scenarios.

    scenarios:
        List of customer counts.

    Example:
        [3, 10, 25, 50]
    """

    if scenarios is None:
        scenarios = [3, 10, 25, 50]

    benchmark_results = []

    for number_of_locations in scenarios:

        # Estimate vehicles conservatively.
        #
        # Average demand is approximately 30,
        # therefore 100-capacity vehicles need
        # roughly one vehicle per 3 customers.
        number_of_vehicles = max(
            2,
            (number_of_locations + 2) // 3
        )

        (
            depot,
            delivery_locations,
            vehicles
        ) = generate_benchmark_data(
            number_of_locations=(
                number_of_locations
            ),
            number_of_vehicles=(
                number_of_vehicles
            ),
            seed=42 + number_of_locations
        )

        result = benchmark_routing_scenario(
            depot=depot,
            delivery_locations=(
                delivery_locations
            ),
            vehicles=vehicles,
            time_limit_seconds=(
                time_limit_seconds
            )
        )

        benchmark_results.append({
            "number_of_locations": (
                number_of_locations
            ),
            "number_of_vehicles": (
                number_of_vehicles
            ),
            **result
        })

    return benchmark_results