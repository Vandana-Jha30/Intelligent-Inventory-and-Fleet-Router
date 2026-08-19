def test_update_inventory_duplicate_returns_conflict(client):
    # 1. Create first warehouse
    response = client.post(
        "/api/warehouses",
        json={
            "name": "Warehouse One",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "capacity": 5000,
            "operating_cost": 25000
        }
    )

    assert response.status_code == 200
    warehouse_1 = response.json()

    # 2. Create second warehouse
    response = client.post(
        "/api/warehouses",
        json={
            "name": "Warehouse Two",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "capacity": 6000,
            "operating_cost": 30000
        }
    )

    assert response.status_code == 200
    warehouse_2 = response.json()

    # 3. Create product
    response = client.post(
        "/api/products",
        json={
            "sku": "API-TEST-001",
            "name": "API Test Product",
            "unit_cost": 100,
            "ordering_cost": 50,
            "holding_cost": 10,
            "lead_time_days": 5,
            "service_level": 0.95
        }
    )

    assert response.status_code == 200
    product = response.json()

    # 4. Create first inventory
    response = client.post(
        "/api/inventory",
        json={
            "warehouse_id": warehouse_1["warehouse_id"],
            "product_id": product["product_id"],
            "on_hand": 100,
            "reserved": 0,
            "on_order": 0
        }
    )

    assert response.status_code == 201

    # 5. Create second inventory
    response = client.post(
        "/api/inventory",
        json={
            "warehouse_id": warehouse_2["warehouse_id"],
            "product_id": product["product_id"],
            "on_hand": 200,
            "reserved": 0,
            "on_order": 0
        }
    )

    assert response.status_code == 201
    inventory_2 = response.json()

    # 6. Try to change Inventory 2 into a duplicate
    response = client.put(
        f"/api/inventory/{inventory_2['inventory_id']}",
        json={
            "warehouse_id": warehouse_1["warehouse_id"],
            "product_id": product["product_id"],
            "on_hand": 200,
            "reserved": 0,
            "on_order": 0
        }
    )

    # 7. Verify conflict
    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Inventory already exists for this product and warehouse"
    )