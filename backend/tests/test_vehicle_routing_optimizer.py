import pytest

from app.optimization.distance_calculator import calculate_distance

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
        demand_quantity,
        latitude=12.9716,
        longitude=77.5946
    ):
        self.demand_quantity = demand_quantity
        self.latitude = latitude
        self.longitude = longitude


class Vehicle:
    def __init__(
        self,
        capacity,
        fixed_cost=1000,
        cost_per_km=20
    ):
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.cost_per_km = cost_per_km


def test_depot_is_required():
    locations = [
        DeliveryLocation(100)
    ]

    vehicles = [
        Vehicle(200)
    ]

    with pytest.raises(
        ValueError,
        match="Depot is required"
    ):
        solve_vehicle_routing(
            None,
            locations,
            vehicles
        )


def test_delivery_location_is_required():
    depot = Depot()

    vehicles = [
        Vehicle(200)
    ]

    with pytest.raises(
        ValueError,
        match="At least one delivery location is required"
    ):
        solve_vehicle_routing(
            depot,
            [],
            vehicles
        )


def test_vehicle_is_required():
    depot = Depot()

    locations = [
        DeliveryLocation(100)
    ]

    with pytest.raises(
        ValueError,
        match="At least one vehicle is required"
    ):
        solve_vehicle_routing(
            depot,
            locations,
            []
        )


def test_insufficient_total_vehicle_capacity():
    depot = Depot()

    locations = [
        DeliveryLocation(300),
        DeliveryLocation(400)
    ]

    vehicles = [
        Vehicle(500)
    ]

    with pytest.raises(
        ValueError,
        match="Total vehicle capacity is insufficient"
    ):
        solve_vehicle_routing(
            depot,
            locations,
            vehicles
        )


def test_feasible_capacity_does_not_raise_validation_error():
    depot = Depot()

    locations = [
        DeliveryLocation(200),
        DeliveryLocation(300)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2

    vehicles = [
        Vehicle(300),
        Vehicle(300)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    assert result["total_distance"] == 0.0
    assert len(result["routes"]) == 2


def test_single_location_demand_exceeds_every_vehicle_capacity():
    depot = Depot()

    locations = [
        DeliveryLocation(800),
        DeliveryLocation(100)
    ]

    vehicles = [
        Vehicle(600),
        Vehicle(600)
    ]

    with pytest.raises(
        ValueError,
        match="A delivery location demand exceeds vehicle capacity"
    ):
        solve_vehicle_routing(
            depot,
            locations,
            vehicles
        )


def test_all_locations_are_assigned():
    depot = Depot()

    locations = [
        DeliveryLocation(100),
        DeliveryLocation(200),
        DeliveryLocation(150)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(300),
        Vehicle(300)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    assigned_location_ids = []

    for route in result["routes"]:
        assigned_location_ids.extend(
            route["location_ids"]
        )

    assert sorted(assigned_location_ids) == [1, 2, 3]


def test_each_location_is_assigned_exactly_once():
    depot = Depot()

    locations = [
        DeliveryLocation(100),
        DeliveryLocation(200),
        DeliveryLocation(150)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(300),
        Vehicle(300)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    assigned_location_ids = []

    for route in result["routes"]:
        assigned_location_ids.extend(
            route["location_ids"]
        )

    assert len(assigned_location_ids) == 3
    assert len(set(assigned_location_ids)) == 3


def test_vehicle_capacity_is_not_exceeded():
    depot = Depot()

    locations = [
        DeliveryLocation(200),
        DeliveryLocation(150),
        DeliveryLocation(100)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(300),
        Vehicle(300)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    vehicle_capacities = {
        1: 300,
        2: 300
    }

    for route in result["routes"]:
        assert (
            route["total_demand"]
            <= vehicle_capacities[route["vehicle_id"]]
        )

        assert route["remaining_capacity"] >= 0


def test_total_assigned_demand_matches_total_location_demand():
    depot = Depot()

    locations = [
        DeliveryLocation(100),
        DeliveryLocation(200),
        DeliveryLocation(150)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(300),
        Vehicle(300)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    total_assigned_demand = sum(
        route["total_demand"]
        for route in result["routes"]
    )

    total_location_demand = sum(
        location.demand_quantity
        for location in locations
    )

    assert total_assigned_demand == total_location_demand


def test_locations_are_assigned_in_decreasing_demand_order():
    depot = Depot()

    locations = [
        DeliveryLocation(100),
        DeliveryLocation(300),
        DeliveryLocation(200)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(500),
        Vehicle(500)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    first_route = result["routes"][0]

    assert first_route["location_ids"] == [2, 3]
    assert first_route["total_demand"] == 500
    assert first_route["remaining_capacity"] == 0


def test_larger_vehicle_is_used_first():
    depot = Depot()

    locations = [
        DeliveryLocation(400),
        DeliveryLocation(200)
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2

    vehicles = [
        Vehicle(300),
        Vehicle(500)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    first_route = result["routes"][0]

    assert first_route["vehicle_id"] == 2
    assert first_route["total_demand"] == 400
    assert first_route["remaining_capacity"] == 100
    assert first_route["location_ids"] == [1]


def test_single_location_route_distance():
    depot = Depot()

    location = DeliveryLocation(
        100,
        latitude=12.9800,
        longitude=77.5946
    )
    location.location_id = 1

    vehicle = Vehicle(200)
    vehicle.vehicle_id = 1

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    expected_one_way_distance = calculate_distance(
        depot.latitude,
        depot.longitude,
        location.latitude,
        location.longitude
    )

    expected_route_distance = (
        expected_one_way_distance * 2
    )

    assert route["route_distance"] == pytest.approx(
        expected_route_distance
    )


def test_two_location_route_distance():
    depot = Depot()

    location_a = DeliveryLocation(
        100,
        latitude=12.9800,
        longitude=77.5946
    )

    location_b = DeliveryLocation(
        100,
        latitude=12.9900,
        longitude=77.5946
    )

    location_a.location_id = 1
    location_b.location_id = 2

    vehicle = Vehicle(300)
    vehicle.vehicle_id = 1

    result = solve_vehicle_routing(
        depot,
        [location_a, location_b],
        [vehicle]
    )

    route = result["routes"][0]

    expected_distance = (
        calculate_distance(
            depot.latitude,
            depot.longitude,
            location_a.latitude,
            location_a.longitude
        )
        +
        calculate_distance(
            location_a.latitude,
            location_a.longitude,
            location_b.latitude,
            location_b.longitude
        )
        +
        calculate_distance(
            location_b.latitude,
            location_b.longitude,
            depot.latitude,
            depot.longitude
        )
    )

    assert route["route_distance"] == pytest.approx(
        expected_distance
    )


def test_total_distance_equals_sum_of_route_distances():
    depot = Depot()

    locations = [
        DeliveryLocation(
            100,
            latitude=12.9800,
            longitude=77.5946
        ),
        DeliveryLocation(
            100,
            latitude=12.9900,
            longitude=77.5946
        ),
        DeliveryLocation(
            100,
            latitude=12.9716,
            longitude=77.6046
        )
    ]

    locations[0].location_id = 1
    locations[1].location_id = 2
    locations[2].location_id = 3

    vehicles = [
        Vehicle(200),
        Vehicle(200)
    ]

    vehicles[0].vehicle_id = 1
    vehicles[1].vehicle_id = 2

    result = solve_vehicle_routing(
        depot,
        locations,
        vehicles
    )

    sum_of_routes = sum(
        route["route_distance"]
        for route in result["routes"]
    )

    assert result["total_distance"] == pytest.approx(
        sum_of_routes
    )


def test_each_route_starts_and_ends_at_depot():
    depot = Depot()

    location = DeliveryLocation(
        100,
        latitude=12.9800,
        longitude=77.5946
    )
    location.location_id = 1

    vehicle = Vehicle(200)
    vehicle.vehicle_id = 1

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    route = result["routes"][0]

    expected_distance = (
        calculate_distance(
            depot.latitude,
            depot.longitude,
            location.latitude,
            location.longitude
        )
        +
        calculate_distance(
            location.latitude,
            location.longitude,
            depot.latitude,
            depot.longitude
        )
    )

    assert route["route_distance"] == pytest.approx(
        expected_distance
    )


def test_route_distance_is_non_negative():
    depot = Depot()

    location = DeliveryLocation(
        100,
        latitude=12.9800,
        longitude=77.5946
    )
    location.location_id = 1

    vehicle = Vehicle(200)
    vehicle.vehicle_id = 1

    result = solve_vehicle_routing(
        depot,
        [location],
        [vehicle]
    )

    for route in result["routes"]:
        assert route["route_distance"] >= 0