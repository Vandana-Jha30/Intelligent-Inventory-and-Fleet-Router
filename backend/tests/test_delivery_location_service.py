import pytest

from app.services.delivery_location_service import (
    create_delivery_location,
    get_delivery_locations,
    get_delivery_location,
    update_delivery_location,
    delete_delivery_location
)

from app.schemas.delivery_location import DeliveryLocationCreate


def test_create_delivery_location(db_session):
    location_data = DeliveryLocationCreate(
        location_name="Customer A",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    location = create_delivery_location(
        db_session,
        location_data
    )

    assert location.location_id is not None
    assert location.location_name == "Customer A"
    assert location.latitude == 12.9716
    assert location.longitude == 77.5946
    assert location.demand_quantity == 500


def test_get_delivery_locations(db_session):
    location_1 = DeliveryLocationCreate(
        location_name="Customer A",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    location_2 = DeliveryLocationCreate(
        location_name="Customer B",
        latitude=13.0827,
        longitude=80.2707,
        demand_quantity=300
    )

    create_delivery_location(db_session, location_1)
    create_delivery_location(db_session, location_2)

    locations = get_delivery_locations(db_session)

    assert len(locations) == 2


def test_get_delivery_location(db_session):
    location_data = DeliveryLocationCreate(
        location_name="Customer A",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    created_location = create_delivery_location(
        db_session,
        location_data
    )

    location = get_delivery_location(
        db_session,
        created_location.location_id
    )

    assert location is not None
    assert location.location_name == "Customer A"


def test_get_nonexistent_delivery_location(db_session):
    location = get_delivery_location(
        db_session,
        99999
    )

    assert location is None


def test_update_delivery_location(db_session):
    location_data = DeliveryLocationCreate(
        location_name="Customer A",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    location = create_delivery_location(
        db_session,
        location_data
    )

    updated_data = DeliveryLocationCreate(
        location_name="Customer A Updated",
        latitude=12.9720,
        longitude=77.5950,
        demand_quantity=750
    )

    updated_location = update_delivery_location(
        db_session,
        location.location_id,
        updated_data
    )

    assert updated_location is not None
    assert updated_location.location_name == "Customer A Updated"
    assert updated_location.demand_quantity == 750


def test_update_nonexistent_delivery_location(db_session):
    location_data = DeliveryLocationCreate(
        location_name="Customer X",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    location = update_delivery_location(
        db_session,
        99999,
        location_data
    )

    assert location is None


def test_delete_delivery_location(db_session):
    location_data = DeliveryLocationCreate(
        location_name="Customer A",
        latitude=12.9716,
        longitude=77.5946,
        demand_quantity=500
    )

    location = create_delivery_location(
        db_session,
        location_data
    )

    deleted = delete_delivery_location(
        db_session,
        location.location_id
    )

    assert deleted is True

    result = get_delivery_location(
        db_session,
        location.location_id
    )

    assert result is None


def test_delete_nonexistent_delivery_location(db_session):
    deleted = delete_delivery_location(
        db_session,
        99999
    )

    assert deleted is False