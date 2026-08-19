from app.services.depot_service import (
    create_depot,
    get_depots,
    get_depot,
    update_depot,
    delete_depot
)

from app.schemas.depot import DepotCreate


def test_create_depot(db_session):
    depot_data = DepotCreate(
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    depot = create_depot(
        db_session,
        depot_data
    )

    assert depot.depot_id is not None
    assert depot.depot_name == "Main Depot"
    assert depot.latitude == 12.9716
    assert depot.longitude == 77.5946


def test_get_depots(db_session):
    depot_1 = DepotCreate(
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    depot_2 = DepotCreate(
        depot_name="Secondary Depot",
        latitude=13.0827,
        longitude=80.2707
    )

    create_depot(db_session, depot_1)
    create_depot(db_session, depot_2)

    depots = get_depots(db_session)

    assert len(depots) == 2


def test_get_depot(db_session):
    depot_data = DepotCreate(
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    created_depot = create_depot(
        db_session,
        depot_data
    )

    depot = get_depot(
        db_session,
        created_depot.depot_id
    )

    assert depot is not None
    assert depot.depot_name == "Main Depot"


def test_get_nonexistent_depot(db_session):
    depot = get_depot(
        db_session,
        99999
    )

    assert depot is None


def test_update_depot(db_session):
    depot_data = DepotCreate(
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    depot = create_depot(
        db_session,
        depot_data
    )

    updated_data = DepotCreate(
        depot_name="Updated Depot",
        latitude=13.0827,
        longitude=80.2707
    )

    updated_depot = update_depot(
        db_session,
        depot.depot_id,
        updated_data
    )

    assert updated_depot is not None
    assert updated_depot.depot_name == "Updated Depot"
    assert updated_depot.latitude == 13.0827
    assert updated_depot.longitude == 80.2707


def test_update_nonexistent_depot(db_session):
    depot_data = DepotCreate(
        depot_name="New Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    depot = update_depot(
        db_session,
        99999,
        depot_data
    )

    assert depot is None


def test_delete_depot(db_session):
    depot_data = DepotCreate(
        depot_name="Main Depot",
        latitude=12.9716,
        longitude=77.5946
    )

    depot = create_depot(
        db_session,
        depot_data
    )

    deleted = delete_depot(
        db_session,
        depot.depot_id
    )

    assert deleted is True

    result = get_depot(
        db_session,
        depot.depot_id
    )

    assert result is None


def test_delete_nonexistent_depot(db_session):
    deleted = delete_depot(
        db_session,
        99999
    )

    assert deleted is False