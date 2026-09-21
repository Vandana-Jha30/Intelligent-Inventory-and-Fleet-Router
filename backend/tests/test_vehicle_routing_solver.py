import pytest
from types import SimpleNamespace

from app.optimization.distance_calculator import calculate_distance

from app.optimization.vehicle_routing_solver import (
    solve_vehicle_routing_optimized
)


def create_depot():
    return SimpleNamespace(
        depot_id=1,
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946
    )


def create_location(
    location_id,
    latitude,
    longitude,
    demand_quantity
):
    return SimpleNamespace(
        location_id=location_id,
        location_name=f"Location {location_id}",
        latitude=latitude,
        longitude=longitude,
        demand_quantity=demand_quantity
    )


def create_vehicle(
    vehicle_id,
    capacity,
    fixed_cost=1000,
    cost_per_km=20
):
    return SimpleNamespace(
        vehicle_id=vehicle_id,
        vehicle_number=f"V-{vehicle_id}",
        capacity=capacity,
        fixed_cost=fixed_cost,
        cost_per_km=cost_per_km
    )


def test_single_delivery_is_served():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    assert result["routes"]

    served_locations = []

    for route in result["routes"]:
        served_locations.extend(
            route["location_ids"]
        )

    assert served_locations == [1]


def test_every_delivery_is_served_exactly_once():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            150
        ),
        create_location(
            3,
            13.0000,
            77.6200,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    served_locations = []

    for route in result["routes"]:
        served_locations.extend(
            route["location_ids"]
        )

    assert sorted(served_locations) == [
        1,
        2,
        3
    ]

    assert len(served_locations) == 3


def test_vehicle_capacity_is_not_exceeded():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            200
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            200
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            400
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    for route in result["routes"]:
        assert (
            route["total_demand"]
            <= 400
        )


def test_multiple_vehicles_can_be_used():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            300
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            300
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            300
        ),
        create_vehicle(
            2,
            300
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    used_routes = [
        route
        for route in result["routes"]
        if route["location_ids"]
    ]

    assert len(used_routes) == 2


def test_unused_vehicle_has_zero_cost():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500,
            fixed_cost=1000,
            cost_per_km=20
        ),
        create_vehicle(
            2,
            500,
            fixed_cost=2000,
            cost_per_km=30
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    unused_routes = [
        route
        for route in result["routes"]
        if not route["location_ids"]
    ]

    assert len(unused_routes) == 1

    assert unused_routes[0]["route_cost"] == 0


def test_fixed_cost_is_included_for_used_vehicle():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500,
            fixed_cost=5000,
            cost_per_km=20
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route = result["routes"][0]

    assert route["location_ids"]

    assert route["route_cost"] >= 5000


def test_route_cost_matches_fixed_plus_distance_cost():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicle = create_vehicle(
        1,
        500,
        fixed_cost=1000,
        cost_per_km=20
    )

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        [vehicle]
    )

    route = result["routes"][0]

    expected_cost = (
        vehicle.fixed_cost
        + (
            vehicle.cost_per_km
            * route["route_distance"]
        )
    )

    assert route["route_cost"] == pytest.approx(
        expected_cost
    )


def test_total_distance_equals_sum_of_route_distances():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            300
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            300
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            300
        ),
        create_vehicle(
            2,
            300
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route_distance_sum = sum(
        route["route_distance"]
        for route in result["routes"]
    )

    assert result["total_distance"] == pytest.approx(
        route_distance_sum
    )


def test_total_cost_equals_sum_of_route_costs():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            300
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            300
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            300
        ),
        create_vehicle(
            2,
            300
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route_cost_sum = sum(
        route["route_cost"]
        for route in result["routes"]
    )

    assert result["total_cost"] == pytest.approx(
        route_cost_sum
    )


def test_total_demand_is_preserved():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            150
        ),
        create_location(
            3,
            13.0000,
            77.6200,
            200
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    total_route_demand = sum(
        route["total_demand"]
        for route in result["routes"]
    )

    expected_demand = sum(
        location.demand_quantity
        for location in locations
    )

    assert total_route_demand == pytest.approx(
        expected_demand
    )


def test_route_distance_is_positive_for_used_vehicle():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route = result["routes"][0]

    assert route["route_distance"] > 0


def test_insufficient_total_capacity_is_rejected():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            400
        ),
        create_location(
            2,
            12.9900,
            77.6100,
            400
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    with pytest.raises(
        ValueError,
        match="Total vehicle capacity is insufficient"
    ):
        solve_vehicle_routing_optimized(
            depot,
            locations,
            vehicles
        )


def test_delivery_larger_than_vehicle_capacity_is_rejected():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            600
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    with pytest.raises(
        ValueError,
        match="A delivery location demand exceeds vehicle capacity"
    ):
        solve_vehicle_routing_optimized(
            depot,
            locations,
            vehicles
        )


def test_depot_is_required():
    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    with pytest.raises(
        ValueError,
        match="Depot is required"
    ):
        solve_vehicle_routing_optimized(
            None,
            locations,
            vehicles
        )


def test_delivery_locations_are_required():
    depot = create_depot()

    vehicles = [
        create_vehicle(
            1,
            500
        )
    ]

    with pytest.raises(
        ValueError,
        match="At least one delivery location is required"
    ):
        solve_vehicle_routing_optimized(
            depot,
            [],
            vehicles
        )


def test_vehicles_are_required():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.9800,
            77.6000,
            100
        )
    ]

    with pytest.raises(
        ValueError,
        match="At least one vehicle is required"
    ):
        solve_vehicle_routing_optimized(
            depot,
            locations,
            []
        )


def test_solver_prefers_fewer_vehicles_when_fixed_costs_apply():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.975,
            77.600,
            100
        ),
        create_location(
            2,
            12.980,
            77.605,
            100
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            300,
            fixed_cost=1000,
            cost_per_km=20
        ),
        create_vehicle(
            2,
            300,
            fixed_cost=1000,
            cost_per_km=20
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    used_routes = [
        route
        for route in result["routes"]
        if route["location_ids"]
    ]

    assert len(used_routes) == 1


def test_solver_visits_every_delivery_exactly_once():
    depot = create_depot()

    locations = [
        create_location(1, 12.975, 77.600, 50),
        create_location(2, 12.980, 77.605, 60),
        create_location(3, 12.985, 77.610, 70),
        create_location(4, 12.990, 77.615, 40),
    ]

    vehicles = [
        create_vehicle(1, 150),
        create_vehicle(2, 150),
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    visited_location_ids = []

    for route in result["routes"]:
        visited_location_ids.extend(
            route["location_ids"]
        )

    assert sorted(visited_location_ids) == [1, 2, 3, 4]
    assert len(visited_location_ids) == 4


def test_solver_does_not_exceed_vehicle_capacity():
    depot = create_depot()

    locations = [
        create_location(1, 12.975, 77.600, 80),
        create_location(2, 12.980, 77.605, 70),
        create_location(3, 12.985, 77.610, 60),
        create_location(4, 12.990, 77.615, 50),
    ]

    vehicles = [
        create_vehicle(1, 150),
        create_vehicle(2, 150),
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    for route in result["routes"]:
        assert route["total_demand"] <= (
            next(
                vehicle.capacity
                for vehicle in vehicles
                if vehicle.vehicle_id == route["vehicle_id"]
            )
        )


def test_solver_routes_start_and_end_at_depot():
    depot = create_depot()

    locations = [
        create_location(1, 12.975, 77.600, 50),
        create_location(2, 12.980, 77.605, 60),
    ]

    vehicles = [
        create_vehicle(1, 150),
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route = result["routes"][0]

    assert route["location_ids"] == [1, 2] or \
           route["location_ids"] == [2, 1]

    expected_distance = 0.0

    current_location = depot

    for location_id in route["location_ids"]:
        location = next(
            location
            for location in locations
            if location.location_id == location_id
        )

        expected_distance += calculate_distance(
            current_location.latitude,
            current_location.longitude,
            location.latitude,
            location.longitude
        )

        current_location = location

    expected_distance += calculate_distance(
        current_location.latitude,
        current_location.longitude,
        depot.latitude,
        depot.longitude
    )

    assert route["route_distance"] == pytest.approx(
        expected_distance,
        abs=1e-6
    )


def test_solver_uses_multiple_vehicles_when_required():
    depot = create_depot()

    locations = [
        create_location(1, 12.975, 77.600, 100),
        create_location(2, 12.980, 77.605, 100),
        create_location(3, 12.985, 77.610, 100),
    ]

    vehicles = [
        create_vehicle(1, 200),
        create_vehicle(2, 200),
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    used_routes = [
        route
        for route in result["routes"]
        if route["location_ids"]
    ]

    assert len(used_routes) == 2

    total_demand = sum(
        route["total_demand"]
        for route in used_routes
    )

    assert total_demand == pytest.approx(300)

    for route in used_routes:
        vehicle = next(
            vehicle
            for vehicle in vehicles
            if vehicle.vehicle_id == route["vehicle_id"]
        )

        assert route["total_demand"] <= vehicle.capacity


def test_solver_considers_vehicle_cost_per_km():
    depot = create_depot()

    locations = [
        create_location(1, 12.975, 77.600, 100),
        create_location(2, 12.980, 77.605, 80),
    ]

    vehicles = [
        create_vehicle(
            1,
            250,
            fixed_cost=1000,
            cost_per_km=100
        ),
        create_vehicle(
            2,
            250,
            fixed_cost=1000,
            cost_per_km=10
        ),
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    used_routes = [
        route
        for route in result["routes"]
        if route["location_ids"]
    ]

    assert len(used_routes) == 1
    assert used_routes[0]["vehicle_id"] == 2


def test_solver_supports_fractional_demand_within_capacity():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.975,
            77.600,
            10.4
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            10.5
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    assert result["routes"][0]["location_ids"] == [1]
    assert result["routes"][0]["total_demand"] == pytest.approx(10.4)


def test_solver_rejects_fractional_demand_above_capacity():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.975,
            77.600,
            10.6
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            10.5
        )
    ]

    with pytest.raises(
        ValueError,
        match="A delivery location demand exceeds vehicle capacity"
    ):
        solve_vehicle_routing_optimized(
            depot,
            locations,
            vehicles
        )


def test_solver_handles_fractional_capacity_exactly():
    depot = create_depot()

    locations = [
        create_location(
            1,
            12.975,
            77.600,
            5.25
        ),
        create_location(
            2,
            12.980,
            77.605,
            5.25
        )
    ]

    vehicles = [
        create_vehicle(
            1,
            10.50
        )
    ]

    result = solve_vehicle_routing_optimized(
        depot,
        locations,
        vehicles
    )

    route = result["routes"][0]

    assert sorted(route["location_ids"]) == [1, 2]
    assert route["total_demand"] == pytest.approx(10.50)
    assert route["remaining_capacity"] == pytest.approx(0.0)