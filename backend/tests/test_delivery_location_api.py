def test_create_delivery_location_api(client):
    response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer A",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["location_id"] is not None
    assert data["location_name"] == "Customer A"
    assert data["latitude"] == 12.9716
    assert data["longitude"] == 77.5946
    assert data["demand_quantity"] == 500


def test_get_all_delivery_locations_api(client):
    client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer A",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer B",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "demand_quantity": 300
        }
    )

    response = client.get("/api/delivery-locations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_get_delivery_location_api(client):
    create_response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer A",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    location_id = create_response.json()["location_id"]

    response = client.get(
        f"/api/delivery-locations/{location_id}"
    )

    assert response.status_code == 200
    assert response.json()["location_name"] == "Customer A"


def test_get_nonexistent_delivery_location_api(client):
    response = client.get(
        "/api/delivery-locations/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Delivery location not found"
    )


def test_update_delivery_location_api(client):
    create_response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer A",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    location_id = create_response.json()["location_id"]

    response = client.put(
        f"/api/delivery-locations/{location_id}",
        json={
            "location_name": "Customer A Updated",
            "latitude": 12.9720,
            "longitude": 77.5950,
            "demand_quantity": 750
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["location_name"] == "Customer A Updated"
    assert data["demand_quantity"] == 750


def test_update_nonexistent_delivery_location_api(client):
    response = client.put(
        "/api/delivery-locations/99999",
        json={
            "location_name": "Customer X",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Delivery location not found"
    )


def test_delete_delivery_location_api(client):
    create_response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Customer A",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    location_id = create_response.json()["location_id"]

    response = client.delete(
        f"/api/delivery-locations/{location_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Delivery location deleted successfully"
    )

    get_response = client.get(
        f"/api/delivery-locations/{location_id}"
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_delivery_location_api(client):
    response = client.delete(
        "/api/delivery-locations/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Delivery location not found"
    )


def test_empty_location_name_returns_validation_error(client):
    response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    assert response.status_code == 422


def test_invalid_latitude_returns_validation_error(client):
    response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Invalid Location",
            "latitude": 91,
            "longitude": 77.5946,
            "demand_quantity": 500
        }
    )

    assert response.status_code == 422


def test_invalid_longitude_returns_validation_error(client):
    response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Invalid Location",
            "latitude": 12.9716,
            "longitude": 181,
            "demand_quantity": 500
        }
    )

    assert response.status_code == 422


def test_negative_demand_returns_validation_error(client):
    response = client.post(
        "/api/delivery-locations",
        json={
            "location_name": "Invalid Demand Location",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "demand_quantity": -100
        }
    )

    assert response.status_code == 422