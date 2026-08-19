def test_create_depot_api(client):
    response = client.post(
        "/api/depots",
        json={
            "depot_name": "Main Depot",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["depot_id"] is not None
    assert data["depot_name"] == "Main Depot"
    assert data["latitude"] == 12.9716
    assert data["longitude"] == 77.5946


def test_get_all_depots_api(client):
    client.post(
        "/api/depots",
        json={
            "depot_name": "Main Depot",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    )

    client.post(
        "/api/depots",
        json={
            "depot_name": "Secondary Depot",
            "latitude": 13.0827,
            "longitude": 80.2707
        }
    )

    response = client.get("/api/depots")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_get_depot_api(client):
    create_response = client.post(
        "/api/depots",
        json={
            "depot_name": "Main Depot",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    )

    depot_id = create_response.json()["depot_id"]

    response = client.get(
        f"/api/depots/{depot_id}"
    )

    assert response.status_code == 200
    assert response.json()["depot_name"] == "Main Depot"


def test_get_nonexistent_depot_api(client):
    response = client.get(
        "/api/depots/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Depot not found"


def test_update_depot_api(client):
    create_response = client.post(
        "/api/depots",
        json={
            "depot_name": "Main Depot",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    )

    depot_id = create_response.json()["depot_id"]

    response = client.put(
        f"/api/depots/{depot_id}",
        json={
            "depot_name": "Updated Depot",
            "latitude": 13.0827,
            "longitude": 80.2707
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["depot_name"] == "Updated Depot"
    assert data["latitude"] == 13.0827
    assert data["longitude"] == 80.2707


def test_update_nonexistent_depot_api(client):
    response = client.put(
        "/api/depots/99999",
        json={
            "depot_name": "Updated Depot",
            "latitude": 13.0827,
            "longitude": 80.2707
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Depot not found"


def test_delete_depot_api(client):
    create_response = client.post(
        "/api/depots",
        json={
            "depot_name": "Main Depot",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    )

    depot_id = create_response.json()["depot_id"]

    response = client.delete(
        f"/api/depots/{depot_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Depot deleted successfully"
    )

    response = client.get(
        f"/api/depots/{depot_id}"
    )

    assert response.status_code == 404


def test_delete_nonexistent_depot_api(client):
    response = client.delete(
        "/api/depots/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Depot not found"