import pytest
from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle
from app.services import supply_chain_service


def test_supply_chain_plan_api_allows_delivery_without_replenishment(
    client,
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    inventory.on_hand = 450
    inventory.on_order = 300
    inventory.reserved = 100

    depot = Depot(
        depot_name="API Test Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    location = DeliveryLocation(
        location_name="API Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=150,
    )

    vehicle = Vehicle(
        vehicle_number="API-SC-001",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([depot, location, vehicle])
    db_session.commit()
    db_session.refresh(depot)
    db_session.refresh(location)

    def fake_solver(depot_arg, locations_arg, vehicles_arg):
        quantity = sum(
            item.demand_quantity
            for item in locations_arg
        )
        return {
            "total_distance": 5.0,
            "total_cost": 150.0,
            "routes": [
                {
                    "vehicle_id": vehicles_arg[0].vehicle_id,
                    "location_ids": [locations_arg[0].location_id],
                    "total_demand": quantity,
                    "remaining_capacity": (
                        vehicles_arg[0].capacity - quantity
                    ),
                    "route_distance": 5.0,
                    "route_cost": 150.0,
                }
            ],
        }

    monkeypatch.setattr(
        supply_chain_service,
        "solve_vehicle_routing_optimized",
        fake_solver,
    )

    response = client.post(
        "/api/supply-chain/plan",
        json={
            "product_id": product.product_id,
            "warehouse_id": warehouse.warehouse_id,
            "depot_id": depot.depot_id,
            "window": 3,
            "delivery_location_ids": [location.location_id],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == product.product_id
    assert data["warehouse_id"] == warehouse.warehouse_id
    assert data["depot_id"] == depot.depot_id
    assert data["inventory_analysis"]["replenishment_required"] is False
    assert data["inventory_analysis"]["recommended_order_quantity"] == 0
    assert data["delivery_demand"] == 150
    assert data["routing"]["routes"][0]["total_demand"] == 150


def test_supply_chain_plan_api_rejects_invalid_location_id(
    client,
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
):
    response = client.post(
        "/api/supply-chain/plan",
        json={
            "product_id": product.product_id,
            "warehouse_id": warehouse.warehouse_id,
            "depot_id": 1,
            "window": 3,
            "delivery_location_ids": [999999],
        },
    )

    assert response.status_code == 404
