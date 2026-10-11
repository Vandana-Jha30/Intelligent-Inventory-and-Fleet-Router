import pytest

from app.models.warehouse import Warehouse
from app.models.delivery_location import DeliveryLocation

from app.optimization.transportation_solver import (
    solve_transportation
)


def test_transportation_solver_finds_optimal_plan():

    warehouse_1 = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    warehouse_1.on_hand = 200
    warehouse_1.reserved = 50

    warehouse_2 = Warehouse(
        warehouse_id=2,
        name="Warehouse 2",
        latitude=12.9800,
        longitude=77.6050,
        capacity=5000,
        operating_cost=25000
    )

    warehouse_2.on_hand = 200
    warehouse_2.reserved = 50

    customer_1 = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    customer_2 = DeliveryLocation(
        location_id=2,
        location_name="Customer B",
        latitude=12.9800,
        longitude=77.6050,
        demand_quantity=100
    )

    result = solve_transportation(
        [warehouse_1, warehouse_2],
        [customer_1, customer_2]
    )

    assert result["total_supply"] == 300
    assert result["total_demand"] == 200

    assert len(
        result["shipment_plan"]
    ) > 0

    total_shipped = sum(
        shipment["quantity"]
        for shipment in result["shipment_plan"]
    )

    assert total_shipped == pytest.approx(
        200
    )


def test_transportation_solver_rejects_insufficient_supply():

    warehouse = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    warehouse.on_hand = 100
    warehouse.reserved = 20

    customer = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    with pytest.raises(
        ValueError,
        match="Total warehouse supply is insufficient"
    ):
        solve_transportation(
            [warehouse],
            [customer]
        )


def test_transportation_solver_rejects_negative_available_inventory():

    warehouse = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    warehouse.on_hand = 50
    warehouse.reserved = 100

    customer = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=20
    )

    with pytest.raises(
        ValueError,
        match="Warehouse available inventory cannot be negative"
    ):
        solve_transportation(
            [warehouse],
            [customer]
        )


def test_transportation_solver_rejects_negative_demand():

    warehouse = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    warehouse.on_hand = 100
    warehouse.reserved = 0

    customer = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=-10
    )

    with pytest.raises(
        ValueError,
        match="Delivery demand cannot be negative"
    ):
        solve_transportation(
            [warehouse],
            [customer]
        )


def test_transportation_solver_requires_warehouse_and_customer():

    with pytest.raises(
        ValueError,
        match="At least one warehouse is required"
    ):
        solve_transportation(
            [],
            []
        )