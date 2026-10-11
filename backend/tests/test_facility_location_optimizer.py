import pytest

from app.models.warehouse import Warehouse
from app.models.delivery_location import DeliveryLocation

from app.optimization.facility_location_optimizer import (
    solve_facility_location
)


def test_facility_location_finds_optimal_plan():

    warehouse_1 = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=200,
        operating_cost=100
    )

    warehouse_2 = Warehouse(
        warehouse_id=2,
        name="Warehouse 2",
        latitude=13.1000,
        longitude=77.7000,
        capacity=200,
        operating_cost=1000
    )

    customer_1 = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    result = solve_facility_location(
        [warehouse_1, warehouse_2],
        [customer_1]
    )

    assert result["total_demand"] == 100

    assert result["facilities_opened"] == 1

    assert result["opened_facilities"][0]["warehouse_id"] == 1

    assert result["allocation_plan"][0]["warehouse_id"] == 1

    assert result["allocation_plan"][0]["quantity"] == pytest.approx(
        100
    )


def test_facility_location_requires_sufficient_capacity():

    warehouse = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=50,
        operating_cost=100
    )

    customer = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    with pytest.raises(
        ValueError,
        match="Total facility capacity is insufficient"
    ):
        solve_facility_location(
            [warehouse],
            [customer]
        )


def test_facility_location_rejects_negative_demand():

    warehouse = Warehouse(
        warehouse_id=1,
        name="Warehouse 1",
        latitude=12.9716,
        longitude=77.5946,
        capacity=500,
        operating_cost=100
    )

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
        solve_facility_location(
            [warehouse],
            [customer]
        )


def test_facility_location_requires_candidate_warehouse():

    customer = DeliveryLocation(
        location_id=1,
        location_name="Customer A",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    with pytest.raises(
        ValueError,
        match="At least one candidate warehouse is required"
    ):
        solve_facility_location(
            [],
            [customer]
        )