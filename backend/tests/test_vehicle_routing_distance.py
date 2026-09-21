from types import SimpleNamespace

import pytest

from app.optimization.vehicle_routing_optimizer import (
    solve_vehicle_routing
)


def create_depot():
    return SimpleNamespace(
        depot_id=1,
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946
    )


def create_vehicle(vehicle_id=1, capacity=500):
    return SimpleNamespace(
        vehicle_id=vehicle_id,
        vehicle_number=f"KA-01-{vehicle_id:04d}",
        capacity=capacity,
        fixed_cost=1000,
        cost_per_km=20
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


def test_single_delivery_route_has_positive_distance():
    depot = create_depot()

    location = create_location(
        location_id=1,
        latitude=13.0827,
        longitude=80.2707,
        demand_quantity=100
    )

    vehicle = create_vehicle(
        vehicle_id=1,
        capacity=500
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    assert route["route_distance"] > 0
    assert result["total_distance"] > 0


def test_single_delivery_route_returns_to_depot():
    depot = create_depot()

    location = create_location(
        location_id=1,
        latitude=13.0827,
        longitude=80.2707,
        demand_quantity=100
    )

    vehicle = create_vehicle(
        vehicle_id=1,
        capacity=500
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    # For one delivery:
    #
    # Depot -> Location -> Depot
    #
    # Therefore:
    # route distance = 2 × one-way distance

    from app.optimization.distance_calculator import (
        calculate_distance
    )

    one_way_distance = calculate_distance(
        depot.latitude,
        depot.longitude,
        location.latitude,
        location.longitude
    )

    expected_distance = 2 * one_way_distance

    assert route["route_distance"] == pytest.approx(
        expected_distance,
        rel=1e-6
    )


def test_multiple_delivery_route_has_distance():
    depot = create_depot()

    locations = [
        create_location(
            location_id=1,
            latitude=13.0827,
            longitude=80.2707,
            demand_quantity=100
        ),
        create_location(
            location_id=2,
            latitude=12.2958,
            longitude=76.6394,
            demand_quantity=100
        ),
        create_location(
            location_id=3,
            latitude=11.0168,
            longitude=76.9558,
            demand_quantity=100
        )
    ]

    vehicle = create_vehicle(
        vehicle_id=1,
        capacity=500
    )

    result = solve_vehicle_routing(
        depot,
        locations,
        [vehicle]
    )

    route = result["routes"][0]

    assert len(route["location_ids"]) == 3
    assert route["route_distance"] > 0
    assert result["total_distance"] > 0


def test_total_distance_equals_sum_of_route_distances():
    depot = create_depot()

    locations = [
        create_location(
            location_id=1,
            latitude=13.0827,
            longitude=80.2707,
            demand_quantity=100
        ),
        create_location(
            location_id=2,
            latitude=12.2958,
            longitude=76.6394,
            demand_quantity=100
        ),
        create_location(
            location_id=3,
            latitude=11.0168,
            longitude=76.9558,
            demand_quantity=100
        )
    ]

    vehicles = [
        create_vehicle(
            vehicle_id=1,
            capacity=200
        ),
        create_vehicle(
            vehicle_id=2,
            capacity=200
        )
    ]

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    route_distance_sum = sum(
        route["route_distance"]
        for route in result["routes"]
    )

    assert result["total_distance"] == pytest.approx(
        route_distance_sum,
        rel=1e-6
    )


def test_empty_vehicle_route_has_zero_distance():
    depot = create_depot()

    locations = [
        create_location(
            location_id=1,
            latitude=13.0827,
            longitude=80.2707,
            demand_quantity=100
        )
    ]

    vehicles = [
        create_vehicle(
            vehicle_id=1,
            capacity=500
        ),
        create_vehicle(
            vehicle_id=2,
            capacity=500
        )
    ]

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    empty_routes = [
        route
        for route in result["routes"]
        if not route["location_ids"]
    ]

    assert len(empty_routes) == 1
    assert empty_routes[0]["route_distance"] == 0