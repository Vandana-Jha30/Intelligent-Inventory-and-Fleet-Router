def test_demand_forecast_api(
    client,
    product,
    warehouse,
    demand_history
):
    response = client.get(
        f"/api/demand/forecast/"
        f"{product.product_id}/"
        f"{warehouse.warehouse_id}?window=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == product.product_id
    assert data["warehouse_id"] == warehouse.warehouse_id
    assert data["method"] == "moving_average"
    assert data["window"] == 3

    assert data["forecast"] == 103.33333333333333