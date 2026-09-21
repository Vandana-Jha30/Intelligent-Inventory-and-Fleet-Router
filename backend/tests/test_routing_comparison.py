from types import SimpleNamespace

import pytest

from app.optimization.routing_comparison import (
    compare_vehicle_routing
)


@pytest.fixture
def depot():
    return SimpleNamespace(
        depot_id=1,
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )


@pytest.fixture
def delivery_locations():
    return [
        SimpleNamespace(
            location_id=1,
            location_name="Customer A",
            latitude=12.975,
            longitude=77.6,
            demand_quantity=50
        ),
        SimpleNamespace(
            location_id=2,
            location_name="Customer B",
            latitude=12.98,
            longitude=77.605,
            demand_quantity=60
        ),
        SimpleNamespace(
            location_id=3,
            location_name="Customer C",
            latitude=12.965,
            longitude=77.59,
            demand_quantity=40
        )
    ]


@pytest.fixture
def vehicles():
    return [
        SimpleNamespace(
            vehicle_id=1,
            vehicle_number="TRUCK-001",
            capacity=100,
            fixed_cost=500,
            cost_per_km=20
        ),
        SimpleNamespace(
            vehicle_id=2,
            vehicle_number="TRUCK-002",
            capacity=100,
            fixed_cost=500,
            cost_per_km=20
        )
    ]


def test_routing_comparison_returns_both_solutions(
    depot,
    delivery_locations,
    vehicles
):
    result = compare_vehicle_routing(
        depot,
        delivery_locations,
        vehicles
    )

    assert "heuristic" in result
    assert "ortools" in result
    assert "comparison" in result


def test_routing_comparison_serves_all_customers(
    depot,
    delivery_locations,
    vehicles
):
    result = compare_vehicle_routing(
        depot,
        delivery_locations,
        vehicles
    )

    for method in ["heuristic", "ortools"]:

        routes = result[method]["routes"]

        served_locations = []

        for route in routes:
            served_locations.extend(
                route["location_ids"]
            )

        assert sorted(served_locations) == [1, 2, 3]


def test_routing_comparison_respects_capacity(
    depot,
    delivery_locations,
    vehicles
):
    result = compare_vehicle_routing(
        depot,
        delivery_locations,
        vehicles
    )

    for method in ["heuristic", "ortools"]:

        for route in result[method]["routes"]:

            assert (
                route["total_demand"]
                <= route["total_demand"]
                + route["remaining_capacity"]
            )


def test_routing_comparison_has_valid_metrics(
    depot,
    delivery_locations,
    vehicles
):
    result = compare_vehicle_routing(
        depot,
        delivery_locations,
        vehicles
    )

    for method in ["heuristic", "ortools"]:

        data = result[method]

        assert data["vehicles_used"] >= 1
        assert data["total_distance"] >= 0
        assert data["total_cost"] >= 0
        assert data["capacity_utilization"] > 0
        assert data["execution_time_ms"] >= 0


def test_routing_comparison_has_difference_metrics(
    depot,
    delivery_locations,
    vehicles
):
    result = compare_vehicle_routing(
        depot,
        delivery_locations,
        vehicles
    )

    comparison = result["comparison"]

    assert "distance_difference" in comparison
    assert "cost_difference" in comparison
    assert "cost_difference_percent" in comparison