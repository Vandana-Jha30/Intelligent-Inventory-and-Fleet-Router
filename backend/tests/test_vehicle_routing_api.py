import pytest

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle


def test_compare_vehicle_routing_api(
    client,
    db_session
):
    # Create depot

    depot = Depot(
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    db_session.add(depot)
    db_session.commit()
    db_session.refresh(depot)

    # Create delivery locations

    locations = [
        DeliveryLocation(
            location_name="Customer A",
            latitude=12.975,
            longitude=77.6,
            demand_quantity=50
        ),
        DeliveryLocation(
            location_name="Customer B",
            latitude=12.98,
            longitude=77.605,
            demand_quantity=60
        ),
        DeliveryLocation(
            location_name="Customer C",
            latitude=12.965,
            longitude=77.59,
            demand_quantity=40
        )
    ]

    db_session.add_all(locations)
    db_session.commit()

    # Create vehicles

    vehicles = [
        Vehicle(
            vehicle_number="TEST-TRUCK-001",
            capacity=100,
            fixed_cost=500,
            cost_per_km=20
        ),
        Vehicle(
            vehicle_number="TEST-TRUCK-002",
            capacity=100,
            fixed_cost=500,
            cost_per_km=20
        )
    ]

    db_session.add_all(vehicles)
    db_session.commit()

    # Call comparison endpoint

    response = client.post(
        "/api/vehicle-routing/compare",
        json={
            "depot_id": depot.depot_id
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Both routing approaches must be present

    assert "heuristic" in data
    assert "ortools" in data
    assert "comparison" in data

    # Both approaches must serve all customers

    for method in ["heuristic", "ortools"]:

        routes = data[method]["routes"]

        served_locations = []

        for route in routes:
            served_locations.extend(
                route["location_ids"]
            )

        assert sorted(served_locations) == [
            locations[0].location_id,
            locations[1].location_id,
            locations[2].location_id
        ]

    # Basic metric validation

    assert data["heuristic"]["vehicles_used"] >= 1
    assert data["ortools"]["vehicles_used"] >= 1

    assert data["heuristic"]["total_distance"] > 0
    assert data["ortools"]["total_distance"] > 0

    assert data["heuristic"]["total_cost"] > 0
    assert data["ortools"]["total_cost"] > 0

    assert data["heuristic"]["execution_time_ms"] >= 0
    assert data["ortools"]["execution_time_ms"] >= 0

    # Comparison metrics

    assert "distance_difference" in data["comparison"]
    assert "cost_difference" in data["comparison"]
    assert "cost_difference_percent" in data["comparison"]


def test_compare_vehicle_routing_api_depot_not_found(
    client
):
    response = client.post(
        "/api/vehicle-routing/compare",
        json={
            "depot_id": 99999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Depot not found"