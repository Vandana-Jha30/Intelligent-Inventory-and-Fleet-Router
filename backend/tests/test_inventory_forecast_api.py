import pytest


def test_inventory_forecast_analysis_api(
    client,
    product,
    warehouse,
    inventory,
    demand_history
):
    response = client.get(
        f"/api/inventory/forecast-analysis/"
        f"{product.product_id}/"
        f"{warehouse.warehouse_id}?window=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == product.product_id
    assert data["warehouse_id"] == warehouse.warehouse_id

    assert data["forecast_daily_demand"] == pytest.approx(
        103.33333333333333
    )

    assert data["annual_demand"] == pytest.approx(
        103.33333333333333 * 365
    )

    assert data["eoq"] > 0
    assert data["safety_stock"] > 0
    assert data["reorder_point"] > 0

    assert data["inventory_position"] == 650
    assert data["replenishment_required"] is False
    assert data["recommended_order_quantity"] == 0