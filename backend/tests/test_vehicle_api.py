def test_create_vehicle_api(client):
    response = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["vehicle_id"] is not None
    assert data["vehicle_number"] == "API-TRUCK-001"
    assert data["capacity"] == 5000
    assert data["fixed_cost"] == 1000
    assert data["cost_per_km"] == 20


def test_get_vehicle_api(client):
    create_response = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    assert create_response.status_code == 201

    vehicle_id = create_response.json()["vehicle_id"]

    response = client.get(
        f"/api/vehicles/{vehicle_id}"
    )

    assert response.status_code == 200
    assert response.json()["vehicle_number"] == "API-TRUCK-001"


def test_get_nonexistent_vehicle_api_returns_404(client):
    response = client.get(
        "/api/vehicles/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


def test_create_duplicate_vehicle_api_returns_409(client):
    vehicle_data = {
        "vehicle_number": "API-TRUCK-001",
        "capacity": 5000,
        "fixed_cost": 1000,
        "cost_per_km": 20
    }

    response = client.post(
        "/api/vehicles",
        json=vehicle_data
    )

    assert response.status_code == 201

    response = client.post(
        "/api/vehicles",
        json=vehicle_data
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Vehicle with this vehicle number already exists"
    )


def test_delete_vehicle_api(client):
    create_response = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    assert create_response.status_code == 201

    vehicle_id = create_response.json()["vehicle_id"]

    response = client.delete(
        f"/api/vehicles/{vehicle_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Vehicle deleted successfully"
    )

    # Verify it no longer exists
    response = client.get(
        f"/api/vehicles/{vehicle_id}"
    )

    assert response.status_code == 404


def test_get_all_vehicles_api(client):
    client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-002",
            "capacity": 3000,
            "fixed_cost": 800,
            "cost_per_km": 15
        }
    )

    response = client.get("/api/vehicles")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_update_vehicle_api(client):
    create_response = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    vehicle_id = create_response.json()["vehicle_id"]

    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={
            "vehicle_number": "API-TRUCK-001-UPDATED",
            "capacity": 6000,
            "fixed_cost": 1200,
            "cost_per_km": 25
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["vehicle_number"] == "API-TRUCK-001-UPDATED"
    assert data["capacity"] == 6000
    assert data["fixed_cost"] == 1200
    assert data["cost_per_km"] == 25


def test_update_nonexistent_vehicle_api_returns_404(client):
    response = client.put(
        "/api/vehicles/99999",
        json={
            "vehicle_number": "NONEXISTENT",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


def test_update_vehicle_to_duplicate_number_api_returns_409(client):
    response_1 = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 5000,
            "fixed_cost": 1000,
            "cost_per_km": 20
        }
    )

    response_2 = client.post(
        "/api/vehicles",
        json={
            "vehicle_number": "API-TRUCK-002",
            "capacity": 3000,
            "fixed_cost": 800,
            "cost_per_km": 15
        }
    )

    vehicle_2_id = response_2.json()["vehicle_id"]

    response = client.put(
        f"/api/vehicles/{vehicle_2_id}",
        json={
            "vehicle_number": "API-TRUCK-001",
            "capacity": 3000,
            "fixed_cost": 800,
            "cost_per_km": 15
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Vehicle with this vehicle number already exists"
    )


def test_delete_nonexistent_vehicle_api_returns_404(client):
    response = client.delete(
        "/api/vehicles/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"