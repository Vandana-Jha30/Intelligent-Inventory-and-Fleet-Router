import pytest

from app.optimization.vehicle_routing_optimizer import (
    solve_vehicle_routing
)


class Depot:
    def __init__(self):
        self.latitude = 12.9716
        self.longitude = 77.5946


class DeliveryLocation:
    def __init__(
        self,
        location_id,
        demand_quantity,
        latitude=12.9800,
        longitude=77.5946
    ):
        self.location_id = location_id
        self.demand_quantity = demand_quantity
        self.latitude = latitude
        self.longitude = longitude


class Vehicle:
    def __init__(
        self,
        vehicle_id,
        capacity,
        fixed_cost=1000,
        cost_per_km=20
    ):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.cost_per_km = cost_per_km


def test_used_vehicle_route_cost_includes_fixed_cost():
    depot = Depot()

    location = DeliveryLocation(
        location_id=1,
        demand_quantity=100
    )

    vehicle = Vehicle(
        vehicle_id=1,
        capacity=200,
        fixed_cost=1000,
        cost_per_km=20
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    expected_cost = (
        vehicle.fixed_cost
        + vehicle.cost_per_km * route["route_distance"]
    )

    assert route["route_cost"] == pytest.approx(
        expected_cost
    )


def test_route_cost_is_distance_cost_plus_fixed_cost():
    depot = Depot()

    location = DeliveryLocation(
        location_id=1,
        demand_quantity=100
    )

    vehicle = Vehicle(
        vehicle_id=1,
        capacity=200,
        fixed_cost=500,
        cost_per_km=10
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    distance_cost = (
        vehicle.cost_per_km
        * route["route_distance"]
    )

    expected_cost = (
        vehicle.fixed_cost
        + distance_cost
    )

    assert route["route_cost"] == pytest.approx(
        expected_cost
    )


def test_unused_vehicle_has_zero_route_cost():
    depot = Depot()

    location = DeliveryLocation(
        location_id=1,
        demand_quantity=100
    )

    vehicles = [
        Vehicle(
            vehicle_id=1,
            capacity=200,
            fixed_cost=1000,
            cost_per_km=20
        ),
        Vehicle(
            vehicle_id=2,
            capacity=500,
            fixed_cost=2000,
            cost_per_km=30
        )
    ]

    result = solve_vehicle_routing(
        depot,
        [location],
        vehicles
    )

    unused_routes = [
        route
        for route in result["routes"]
        if not route["location_ids"]
    ]

    assert len(unused_routes) == 1
    assert unused_routes[0]["route_cost"] == 0.0


def test_total_cost_equals_sum_of_route_costs():
    depot = Depot()

    locations = [
        DeliveryLocation(
            location_id=1,
            demand_quantity=100,
            latitude=12.9800,
            longitude=77.5946
        ),
        DeliveryLocation(
            location_id=2,
            demand_quantity=100,
            latitude=12.9900,
            longitude=77.5946
        ),
        DeliveryLocation(
            location_id=3,
            demand_quantity=100,
            latitude=12.9716,
            longitude=77.6046
        )
    ]

    vehicles = [
        Vehicle(
            vehicle_id=1,
            capacity=200,
            fixed_cost=1000,
            cost_per_km=20
        ),
        Vehicle(
            vehicle_id=2,
            capacity=200,
            fixed_cost=1500,
            cost_per_km=25
        )
    ]

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    sum_of_route_costs = sum(
        route["route_cost"]
        for route in result["routes"]
    )

    assert result["total_cost"] == pytest.approx(
        sum_of_route_costs
    )


def test_zero_cost_per_km_uses_only_fixed_cost():
    depot = Depot()

    location = DeliveryLocation(
        location_id=1,
        demand_quantity=100
    )

    vehicle = Vehicle(
        vehicle_id=1,
        capacity=200,
        fixed_cost=1000,
        cost_per_km=0
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    assert route["route_cost"] == pytest.approx(
        vehicle.fixed_cost
    )


def test_zero_fixed_cost_uses_only_distance_cost():
    depot = Depot()

    location = DeliveryLocation(
        location_id=1,
        demand_quantity=100
    )

    vehicle = Vehicle(
        vehicle_id=1,
        capacity=200,
        fixed_cost=0,
        cost_per_km=20
    )

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    expected_cost = (
        vehicle.cost_per_km
        * route["route_distance"]
    )

    assert route["route_cost"] == pytest.approx(
        expected_cost
    )