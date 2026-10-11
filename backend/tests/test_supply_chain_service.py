import pytest

from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle
from app.services import supply_chain_service

from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.optimization.warehouse_allocation import (
    nearest_warehouse_allocation,
)
from app.optimization.min_cost_flow_solver import solve_min_cost_flow
from app.schemas.min_cost_flow import (
    FlowNodeRequest,
    FlowArcRequest,
)
from types import SimpleNamespace


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



def test_supply_chain_plan_uses_multiple_warehouses_for_min_cost_flow(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    # Existing warehouse
    inventory.on_hand = 200
    inventory.reserved = 0

    # Second warehouse
    warehouse_2 = Warehouse(
        name="Second Warehouse",
        latitude=12.9717,
        longitude=77.5947,
        capacity=5000,
        operating_cost=25000,
    )

    db_session.add(warehouse_2)
    db_session.commit()
    db_session.refresh(warehouse_2)

    inventory_2 = Inventory(
        warehouse_id=warehouse_2.warehouse_id,
        product_id=product.product_id,
        on_hand=200,
        reserved=0,
        on_order=0,
    )

    depot = Depot(
        depot_name="Test Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    location = DeliveryLocation(
        location_name="Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=300,
    )

    vehicle = Vehicle(
        vehicle_number="MULTI-WH-001",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([
        inventory_2,
        depot,
        location,
        vehicle,
    ])
    db_session.commit()
    db_session.refresh(depot)
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
        delivery_location_ids=[location.location_id],
        window=3,
    )

    assert result["delivery_demand"] == 300
    assert result["available_inventory"] == 400

    flow_plan = result["min_cost_flow"]["flow_plan"]

    customer_flows = [
        item
        for item in flow_plan
        if item["to_node"] != 2_000_000
    ]

    assert sum(
        item["flow"]
        for item in customer_flows
    ) == 300

    assert len(customer_flows) == 2

    source_warehouses = {
        item["from_node"]
        for item in customer_flows
    }

    assert source_warehouses == {
        warehouse.warehouse_id,
        warehouse_2.warehouse_id,
    }



def test_supply_chain_plan_returns_warehouse_customer_allocation(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    inventory.on_hand = 200
    inventory.reserved = 0

    warehouse_2 = Warehouse(
        name="Second Warehouse",
        latitude=12.9717,
        longitude=77.5947,
        capacity=5000,
        operating_cost=25000,
    )

    db_session.add(warehouse_2)
    db_session.commit()
    db_session.refresh(warehouse_2)

    inventory_2 = Inventory(
        warehouse_id=warehouse_2.warehouse_id,
        product_id=product.product_id,
        on_hand=200,
        reserved=0,
        on_order=0,
    )

    depot = Depot(
        depot_name="Allocation Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    location = DeliveryLocation(
        location_name="Allocation Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=300,
    )

    vehicle = Vehicle(
        vehicle_number="ALLOC-001",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([
        inventory_2,
        depot,
        location,
        vehicle,
    ])
    db_session.commit()

    db_session.refresh(depot)
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
        delivery_location_ids=[location.location_id],
        window=3,
    )

    allocation = result["allocation"]

    assert len(allocation) == 2

    assert sum(
        item["quantity"]
        for item in allocation
    ) == 300

    assert {
        item["warehouse_id"]
        for item in allocation
    } == {
        warehouse.warehouse_id,
        warehouse_2.warehouse_id,
    }

    assert all(
        item["location_id"] == location.location_id
        for item in allocation
    )

    assert all(
        item["quantity"] > 0
        for item in allocation
    )

    assert all(
        item["distance_km"] >= 0
        for item in allocation
    )

    assert all(
        item["transportation_cost"] >= 0
        for item in allocation
    )


def test_supply_chain_plan_mcf_beats_nearest_warehouse_baseline(
    db_session,
    warehouse,
    product,
    inventory,
    demand_history,
    monkeypatch,
):
    # Warehouse 1 is closer to Customer 1 but has limited inventory.
    inventory.on_hand = 100
    inventory.reserved = 0

    warehouse_2 = Warehouse(
        name="Second Warehouse",
        latitude=13.0000,
        longitude=77.6000,
        capacity=5000,
        operating_cost=25000,
    )

    db_session.add(warehouse_2)
    db_session.commit()
    db_session.refresh(warehouse_2)

    inventory_2 = Inventory(
        warehouse_id=warehouse_2.warehouse_id,
        product_id=product.product_id,
        on_hand=200,
        reserved=0,
        on_order=0,
    )

    depot = Depot(
        depot_name="Comparison Depot",
        latitude=12.9716,
        longitude=77.5946,
    )

    customer_1 = DeliveryLocation(
        location_name="Customer 1",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100,
    )

    customer_2 = DeliveryLocation(
        location_name="Customer 2",
        latitude=12.9900,
        longitude=77.6100,
        demand_quantity=200,
    )

    vehicle = Vehicle(
        vehicle_number="COMPARE-001",
        capacity=1000,
        fixed_cost=100,
        cost_per_km=10,
    )

    db_session.add_all([
        inventory_2,
        depot,
        customer_1,
        customer_2,
        vehicle,
    ])

    db_session.commit()

    db_session.refresh(depot)
    db_session.refresh(customer_1)
    db_session.refresh(customer_2)

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
            customer_1.location_id,
            customer_2.location_id,
        ],
        window=3,
    )

    assert result["delivery_demand"] == 300
    assert result["available_inventory"] == 300

    assert result["baseline_allocation"]["total_flow"] == 300

    assert result["optimized_cost"] <= result["baseline_cost"]

    assert result["cost_improvement_percent"] >= -1e-9



def test_nearest_warehouse_baseline_can_be_suboptimal(
    db_session,
):
    warehouse_1 = Warehouse(
        name="Warehouse 1",
        latitude=0,
        longitude=0,
        capacity=100,
        operating_cost=0,
    )

    warehouse_2 = Warehouse(
        name="Warehouse 2",
        latitude=0,
        longitude=0,
        capacity=200,
        operating_cost=0,
    )

    customer_1 = DeliveryLocation(
        location_name="Customer 1",
        latitude=0,
        longitude=0,
        demand_quantity=100,
    )

    customer_2 = DeliveryLocation(
        location_name="Customer 2",
        latitude=0,
        longitude=0,
        demand_quantity=200,
    )

    db_session.add_all([
        warehouse_1,
        warehouse_2,
        customer_1,
        customer_2,
    ])

    db_session.commit()

    db_session.refresh(warehouse_1)
    db_session.refresh(warehouse_2)
    db_session.refresh(customer_1)
    db_session.refresh(customer_2)

    inventory = {
        warehouse_1.warehouse_id: 100,
        warehouse_2.warehouse_id: 200,
    }

    # Deliberately constructed distance matrix:
    #
    #                 Customer 1   Customer 2
    # Warehouse 1        1            2
    # Warehouse 2        2           100
    #
    # The greedy nearest-warehouse rule processes Customer 1 first:
    #
    # W1 -> C1 = 100
    # W2 -> C2 = 200
    #
    # Cost = 100*1 + 200*100 = 20100
    #
    # But if Customer 1 is assigned to W2 and Customer 2 to W1,
    # the cost would be:
    #
    # W2 -> C1 = 100*2
    # W1 -> C2 = 200*2
    #
    # Total = 600.
    #
    # This demonstrates that a local nearest decision can be
    # globally suboptimal.

    distances = {
        (
            warehouse_1.warehouse_id,
            customer_1.location_id,
        ): 1.0,

        (
            warehouse_1.warehouse_id,
            customer_2.location_id,
        ): 2.0,

        (
            warehouse_2.warehouse_id,
            customer_1.location_id,
        ): 2.0,

        (
            warehouse_2.warehouse_id,
            customer_2.location_id,
        ): 100.0,
    }

    def controlled_distance(warehouse, location):
        return distances[
            (
                warehouse.warehouse_id,
                location.location_id,
            )
        ]

    result = nearest_warehouse_allocation(
        warehouses=[
            warehouse_1,
            warehouse_2,
        ],
        inventory_by_warehouse=inventory,
        delivery_locations=[
            customer_1,
            customer_2,
        ],
        distance_function=controlled_distance,
    )

    assert result["total_flow"] == 300

    assert result["total_cost"] == pytest.approx(
        20100
    )


def test_min_cost_flow_finds_better_global_allocation():
    nodes = [
        FlowNodeRequest(
            node_id=1,
            name="Warehouse 1",
            supply=100,
            demand=0,
        ),
        FlowNodeRequest(
            node_id=2,
            name="Warehouse 2",
            supply=200,
            demand=0,
        ),
        FlowNodeRequest(
            node_id=101,
            name="Customer 1",
            supply=0,
            demand=100,
        ),
        FlowNodeRequest(
            node_id=102,
            name="Customer 2",
            supply=0,
            demand=200,
        ),
    ]

    arcs = [
        FlowArcRequest(
            from_node=1,
            to_node=101,
            capacity=100,
            cost=1,
        ),
        FlowArcRequest(
            from_node=1,
            to_node=102,
            capacity=100,
            cost=2,
        ),
        FlowArcRequest(
            from_node=2,
            to_node=101,
            capacity=100,
            cost=2,
        ),
        FlowArcRequest(
            from_node=2,
            to_node=102,
            capacity=200,
            cost=100,
        ),
    ]

    result = solve_min_cost_flow(
        nodes,
        arcs,
    )

    assert result["total_flow"] == 300

    assert result["total_cost"] == pytest.approx(10400)

    allocation = {
        (
            item["from_node"],
            item["to_node"],
        ): item["flow"]
        for item in result["flow_plan"]
    }

    assert allocation[(1, 102)] == pytest.approx(100)
    assert allocation[(2, 101)] == pytest.approx(100)
    assert allocation[(2, 102)] == pytest.approx(100)

    assert allocation.get((1, 101), 0) == pytest.approx(0)


def test_mcf_beats_nearest_warehouse_baseline():
    warehouses = [
        SimpleNamespace(warehouse_id=1, name="W1"),
        SimpleNamespace(warehouse_id=2, name="W2"),
    ]

    locations = [
        SimpleNamespace(
            location_id=101,
            location_name="C1",
            demand_quantity=100,
        ),
        SimpleNamespace(
            location_id=102,
            location_name="C2",
            demand_quantity=200,
        ),
    ]

    inventory_by_warehouse = {
        1: 100,
        2: 200,
    }

    def controlled_distance(warehouse, location):
        costs = {
            (1, 101): 1,
            (1, 102): 2,
            (2, 101): 2,
            (2, 102): 100,
        }
        return costs[(warehouse.warehouse_id, location.location_id)]

    baseline = nearest_warehouse_allocation(
        warehouses=warehouses,
        inventory_by_warehouse=inventory_by_warehouse,
        delivery_locations=locations,
        distance_function=controlled_distance,
    )

    nodes = [
        FlowNodeRequest(node_id=1, name="W1", supply=100),
        FlowNodeRequest(node_id=2, name="W2", supply=200),
        FlowNodeRequest(node_id=101, name="C1", demand=100),
        FlowNodeRequest(node_id=102, name="C2", demand=200),
    ]

    arcs = [
        FlowArcRequest(from_node=1, to_node=101, capacity=100, cost=1),
        FlowArcRequest(from_node=1, to_node=102, capacity=100, cost=2),
        FlowArcRequest(from_node=2, to_node=101, capacity=100, cost=2),
        FlowArcRequest(from_node=2, to_node=102, capacity=200, cost=100),
    ]

    optimized = solve_min_cost_flow(nodes, arcs)

    assert baseline["total_cost"] == pytest.approx(20100)
    assert optimized["total_cost"] == pytest.approx(10400)

    assert optimized["total_cost"] < baseline["total_cost"]

    improvement = (
        (baseline["total_cost"] - optimized["total_cost"])
        / baseline["total_cost"]
        * 100
    )

    assert improvement == pytest.approx(48.2587, rel=1e-3)