def test_solve_transportation_api(client, db_session):
    from app.models.warehouse import Warehouse
    from app.models.delivery_location import DeliveryLocation

    warehouse = Warehouse(
        name="Transportation Warehouse",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    customer = DeliveryLocation(
        location_name="Transportation Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    db_session.add(warehouse)
    db_session.add(customer)
    db_session.commit()

    db_session.refresh(warehouse)
    db_session.refresh(customer)

    warehouse.on_hand = 200
    warehouse.reserved = 50

    db_session.commit()

    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [warehouse.warehouse_id],
            "delivery_location_ids": [
                customer.location_id
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_supply"] == 150
    assert data["total_demand"] == 100

    assert len(data["shipment_plan"]) == 1

    shipment = data["shipment_plan"][0]

    assert shipment["warehouse_id"] == warehouse.warehouse_id
    assert shipment["location_id"] == customer.location_id
    assert shipment["quantity"] == 100

    assert len(data["warehouse_summary"]) == 1

    summary = data["warehouse_summary"][0]

    assert summary["available_supply"] == 150
    assert summary["shipped_quantity"] == 100
    assert summary["remaining_supply"] == 50



def test_transportation_api_rejects_nonexistent_warehouse(client):
    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [99999],
            "delivery_location_ids": [1]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Warehouse not found: 99999"
    )


def test_transportation_api_rejects_nonexistent_delivery_location(
    client,
    db_session
):
    from app.models.warehouse import Warehouse

    warehouse = Warehouse(
        name="Test Warehouse",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    db_session.add(warehouse)
    db_session.commit()

    db_session.refresh(warehouse)

    warehouse.on_hand = 500
    warehouse.reserved = 0

    db_session.commit()

    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [warehouse.warehouse_id],
            "delivery_location_ids": [99999]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Delivery location not found: 99999"
    )


def test_transportation_api_rejects_duplicate_warehouse_ids(
    client
):
    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [1, 1],
            "delivery_location_ids": [1]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Each warehouse can appear only once"
    )


def test_transportation_api_rejects_duplicate_delivery_location_ids(
    client,
    db_session
):
    from app.models.warehouse import Warehouse
    from app.models.delivery_location import DeliveryLocation

    warehouse = Warehouse(
        name="Duplicate Test Warehouse",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    customer = DeliveryLocation(
        location_name="Duplicate Test Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=100
    )

    db_session.add(warehouse)
    db_session.add(customer)
    db_session.commit()

    db_session.refresh(warehouse)
    db_session.refresh(customer)

    warehouse.on_hand = 200
    warehouse.reserved = 0

    db_session.commit()

    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [warehouse.warehouse_id],
            "delivery_location_ids": [
                customer.location_id,
                customer.location_id
            ]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Each delivery location can appear only once"
    )


def test_transportation_api_rejects_insufficient_supply(
    client,
    db_session
):
    from app.models.warehouse import Warehouse
    from app.models.delivery_location import DeliveryLocation

    warehouse = Warehouse(
        name="Low Supply Warehouse",
        latitude=12.9716,
        longitude=77.5946,
        capacity=5000,
        operating_cost=25000
    )

    customer = DeliveryLocation(
        location_name="Large Demand Customer",
        latitude=12.9750,
        longitude=77.6000,
        demand_quantity=500
    )

    db_session.add(warehouse)
    db_session.add(customer)
    db_session.commit()

    db_session.refresh(warehouse)
    db_session.refresh(customer)

    warehouse.on_hand = 100
    warehouse.reserved = 20

    db_session.commit()

    response = client.post(
        "/api/transportation/solve",
        json={
            "warehouse_ids": [warehouse.warehouse_id],
            "delivery_location_ids": [
                customer.location_id
            ]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Total warehouse supply is insufficient "
        "for customer demand"
    )