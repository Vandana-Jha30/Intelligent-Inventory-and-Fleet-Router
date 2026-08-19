import pytest

from app.services.vehicle_service import (
    create_vehicle,
    get_vehicle,
    get_vehicles,
    update_vehicle,
    delete_vehicle
)

from app.schemas.vehicle import VehicleCreate


def test_create_vehicle(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=20
    )

    vehicle = create_vehicle(
        db_session,
        vehicle_data
    )

    assert vehicle.vehicle_id is not None
    assert vehicle.vehicle_number == "TRUCK-001"
    assert vehicle.capacity == 5000
    assert vehicle.fixed_cost == 1000
    assert vehicle.cost_per_km == 20


def test_create_duplicate_vehicle_raises_error(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=20
    )

    create_vehicle(db_session, vehicle_data)

    with pytest.raises(
        ValueError,
        match="Vehicle with this vehicle number already exists"
    ):
        create_vehicle(db_session, vehicle_data)


def test_create_vehicle_with_invalid_capacity_raises_error(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=0,
        fixed_cost=1000,
        cost_per_km=20
    )

    with pytest.raises(
        ValueError,
        match="Vehicle capacity must be positive"
    ):
        create_vehicle(db_session, vehicle_data)


def test_get_vehicle(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=20
    )

    created_vehicle = create_vehicle(
        db_session,
        vehicle_data
    )

    vehicle = get_vehicle(
        db_session,
        created_vehicle.vehicle_id
    )

    assert vehicle is not None
    assert vehicle.vehicle_number == "TRUCK-001"


def test_get_all_vehicles(db_session):
    vehicle_1 = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=20
    )

    vehicle_2 = VehicleCreate(
        vehicle_number="TRUCK-002",
        capacity=3000,
        fixed_cost=800,
        cost_per_km=15
    )

    create_vehicle(db_session, vehicle_1)
    create_vehicle(db_session, vehicle_2)

    vehicles = get_vehicles(db_session)

    assert len(vehicles) == 2


def test_create_vehicle_with_negative_fixed_cost_raises_error(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=-100,
        cost_per_km=20
    )

    with pytest.raises(
        ValueError,
        match="Fixed cost cannot be negative"
    ):
        create_vehicle(db_session, vehicle_data)


def test_create_vehicle_with_negative_cost_per_km_raises_error(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=-20
    )

    with pytest.raises(
        ValueError,
        match="Cost per km cannot be negative"
    ):
        create_vehicle(db_session, vehicle_data)


def test_update_vehicle(db_session):
    vehicle = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    updated_vehicle = update_vehicle(
        db_session,
        vehicle.vehicle_id,
        VehicleCreate(
            vehicle_number="TRUCK-001-UPDATED",
            capacity=6000,
            fixed_cost=1200,
            cost_per_km=25
        )
    )

    assert updated_vehicle.vehicle_number == "TRUCK-001-UPDATED"
    assert updated_vehicle.capacity == 6000
    assert updated_vehicle.fixed_cost == 1200
    assert updated_vehicle.cost_per_km == 25


def test_update_nonexistent_vehicle_returns_none(db_session):
    vehicle_data = VehicleCreate(
        vehicle_number="TRUCK-001",
        capacity=5000,
        fixed_cost=1000,
        cost_per_km=20
    )

    vehicle = update_vehicle(
        db_session,
        99999,
        vehicle_data
    )

    assert vehicle is None


def test_update_vehicle_to_duplicate_number_raises_error(db_session):
    vehicle_1 = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    vehicle_2 = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-002",
            capacity=3000,
            fixed_cost=800,
            cost_per_km=15
        )
    )

    with pytest.raises(
        ValueError,
        match="Vehicle with this vehicle number already exists"
    ):
        update_vehicle(
            db_session,
            vehicle_2.vehicle_id,
            VehicleCreate(
                vehicle_number=vehicle_1.vehicle_number,
                capacity=3000,
                fixed_cost=800,
                cost_per_km=15
            )
        )


def test_delete_vehicle(db_session):
    vehicle = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    deleted = delete_vehicle(
        db_session,
        vehicle.vehicle_id
    )

    assert deleted is True

    assert get_vehicle(
        db_session,
        vehicle.vehicle_id
    ) is None


def test_delete_nonexistent_vehicle_returns_false(db_session):
    deleted = delete_vehicle(
        db_session,
        99999
    )

    assert deleted is False


def test_update_vehicle_with_zero_capacity_raises_error(db_session):
    vehicle = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    with pytest.raises(
        ValueError,
        match="Vehicle capacity must be positive"
    ):
        update_vehicle(
            db_session,
            vehicle.vehicle_id,
            VehicleCreate(
                vehicle_number="TRUCK-001",
                capacity=0,
                fixed_cost=1000,
                cost_per_km=20
            )
        )


def test_update_vehicle_with_negative_fixed_cost_raises_error(db_session):
    vehicle = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    with pytest.raises(
        ValueError,
        match="Fixed cost cannot be negative"
    ):
        update_vehicle(
            db_session,
            vehicle.vehicle_id,
            VehicleCreate(
                vehicle_number="TRUCK-001",
                capacity=5000,
                fixed_cost=-100,
                cost_per_km=20
            )
        )


def test_update_vehicle_with_negative_cost_per_km_raises_error(db_session):
    vehicle = create_vehicle(
        db_session,
        VehicleCreate(
            vehicle_number="TRUCK-001",
            capacity=5000,
            fixed_cost=1000,
            cost_per_km=20
        )
    )

    with pytest.raises(
        ValueError,
        match="Cost per km cannot be negative"
    ):
        update_vehicle(
            db_session,
            vehicle.vehicle_id,
            VehicleCreate(
                vehicle_number="TRUCK-001",
                capacity=5000,
                fixed_cost=1000,
                cost_per_km=-20
            )
        )