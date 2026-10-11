def test_solve_facility_location_api(client):
    warehouse_1 = client.post(
        "/api/warehouses",
        json={
            "name": "Warehouse FL 1",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "capacity": 5000,
            "operating_cost": 100
        }
    )

    assert warehouse_1.status_code == 201

    warehouse_2 = client.post(
        "/api/warehouses",
        json={
            "name": "Warehouse FL 2",
            "latitude": 13.1000,
            "longitude": 77.7000,
            "capacity": 5000,
            "operating_cost": 1000
        }
    )

    assert warehouse_2.status_code == 201

    location = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer FL 1",
            "latitude": 12.9750,
            "longitude": 77.6000,
            "demand_quantity": 100
        }
    )

    assert location.status_code == 201

    warehouse_id_1 = warehouse_1.json()["warehouse_id"]
    warehouse_id_2 = warehouse_2.json()["warehouse_id"]
    location_id = location.json()["location_id"]

    response = client.post(
        "/api/facility-location/solve",
        json={
            "warehouse_ids": [
                warehouse_id_1,
                warehouse_id_2
            ],
            "delivery_location_ids": [
                location_id
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_demand"] == 100
    assert data["facilities_opened"] >= 1
    assert data["total_cost"] >= 0
    assert len(data["opened_facilities"]) >= 1
    assert len(data["allocation_plan"]) >= 1


def test_facility_location_api_rejects_duplicate_warehouse_ids(
    client
):
    response = client.post(
        "/api/facility-location/solve",
        json={
            "warehouse_ids": [1, 1],
            "delivery_location_ids": [1]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Each warehouse ID can appear only once"
    )


def test_facility_location_api_rejects_duplicate_delivery_location_ids(
    client
):
    response = client.post(
        "/api/facility-location/solve",
        json={
            "warehouse_ids": [1],
            "delivery_location_ids": [1, 1]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Each delivery location ID can appear only once"
    )


def test_facility_location_api_rejects_nonexistent_warehouse(
    client
):
    response = client.post(
        "/api/facility-location/solve",
        json={
            "warehouse_ids": [99999],
            "delivery_location_ids": [1]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Warehouse not found: 99999"
    )


def test_facility_location_api_rejects_nonexistent_delivery_location(
    client
):
    response = client.post(
        "/api/facility-location/solve",
        json={
            "warehouse_ids": [1],
            "delivery_location_ids": [99999]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Delivery location not found: 99999"
    )