import pytest

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle
from app.services import supply_chain_service


def _fake_routing_solver(depot_arg, locations_arg, vehicles_arg):
    demand = sum(
        location.demand_quantity
        for location in locations_arg
    )

    return {
        "total_distance": 10.0,
        "total_cost": 200.0,
        "routes": [
            {
                "vehicle_id": vehicles_arg[0].vehicle_id,
                "location_ids": [
                    location.location_id
                    for location in locations_arg
                ],
                "total_demand": demand,
                "remaining_capacity": (
                    vehicles_arg[0].capacity - demand
                ),
                "route_distance": 10.0,
                "route_cost": 200.0,
            }
        ],
    }


def test_supply_chain_plan_keeps_replenishment_separate_from_distribution(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    # This mirrors the real database scenario: inventory is above ROP, so no
    # supplier replenishment is required, while customers still have demand.
    inventory.on_hand = 450
    inventory.reserved = 100
    inventory.on_order = 300

    depot = Depot(
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    location_1 = DeliveryLocation(
        location_name="Customer 1",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=50,
    )

    location_2 = DeliveryLocation(
        location_name="Customer 2",
        latitude=12.9800,
        longitude=77.6050,
        demand_quantity=60,
    )

    vehicle = Vehicle(
        vehicle_number="TEST-SC-001",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([depot, location_1, location_2, vehicle])
    db_session.commit()
    db_session.refresh(depot)
    db_session.refresh(location_1)
    db_session.refresh(location_2)

    monkeypatch.setattr(
        supply_chain_service,
        "solve_vehicle_routing_optimized",
        _fake_routing_solver,
    )

    result = supply_chain_service.create_supply_chain_plan(
        db=db_session,
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id,
        depot_id=depot.depot_id,
        delivery_location_ids=[
            location_1.location_id,
            location_2.location_id,
        ],
        window=3,
    )

    assert result["inventory_analysis"]["replenishment_required"] is False
    assert result["inventory_analysis"]["recommended_order_quantity"] == 0
    assert result["delivery_demand"] == 110
    assert result["routing"]["routes"][0]["total_demand"] == 110


def test_supply_chain_plan_routes_selected_locations_only(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    depot = Depot(
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    locations = [
        DeliveryLocation(
            location_name="Customer 1",
            latitude=12.9750,
            longitude=77.6000,
            demand_quantity=50,
        ),
        DeliveryLocation(
            location_name="Customer 2",
            latitude=12.9800,
            longitude=77.6050,
            demand_quantity=60,
        ),
    ]

    vehicle = Vehicle(
        vehicle_number="TEST-SC-002",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([depot, *locations, vehicle])
    db_session.commit()
    db_session.refresh(depot)
    for location in locations:
        db_session.refresh(location)

    monkeypatch.setattr(
        supply_chain_service,
        "solve_vehicle_routing_optimized",
        _fake_routing_solver,
    )

    result = supply_chain_service.create_supply_chain_plan(
        db=db_session,
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id,
        depot_id=depot.depot_id,
        delivery_location_ids=[locations[1].location_id],
        window=3,
    )

    assert result["delivery_demand"] == 60
    assert result["routing"]["routes"][0]["location_ids"] == [
        locations[1].location_id
    ]


def test_supply_chain_plan_rejects_duplicate_locations(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
):
    depot = Depot(
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    location = DeliveryLocation(
        location_name="Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100,
    )

    db_session.add_all([depot, location])
    db_session.commit()
    db_session.refresh(depot)
    db_session.refresh(location)

    try:
        supply_chain_service.create_supply_chain_plan(
            db=db_session,
            product_id=product.product_id,
            warehouse_id=warehouse.warehouse_id,
            depot_id=depot.depot_id,
            delivery_location_ids=[
                location.location_id,
                location.location_id,
            ],
            window=3,
        )
    except ValueError as error:
        assert str(error) == "Each delivery location can appear only once"
    else:
        raise AssertionError("Expected duplicate location validation error")
