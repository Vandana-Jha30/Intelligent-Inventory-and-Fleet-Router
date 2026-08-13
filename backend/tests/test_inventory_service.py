import pytest

from app.services.inventory_service import analyze_inventory


def test_inventory_analysis(
    db_session,
    product,
    warehouse,
    inventory,
    demand_history
):
    result = analyze_inventory(
        db_session,
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id
    )

    assert result["average_daily_demand"] == 102
    assert result["annual_demand"] == 37230

    assert result["on_hand"] == 450
    assert result["reserved"] == 100
    assert result["on_order"] == 300

    assert result["inventory_position"] == 650

    assert result["replenishment_required"] is False
    assert result["recommended_order_quantity"] == 0


def test_missing_inventory(
    db_session,
    product,
    warehouse,
    demand_history
):
    with pytest.raises(
        ValueError,
        match="Inventory record not found"
    ):
        analyze_inventory(
            db_session,
            product_id=product.product_id,
            warehouse_id=warehouse.warehouse_id
        )


def test_insufficient_demand_history(
    db_session,
    product,
    warehouse,
    inventory
):
    with pytest.raises(
        ValueError,
        match="At least two demand records are required"
    ):
        analyze_inventory(
            db_session,
            product_id=product.product_id,
            warehouse_id=warehouse.warehouse_id
        )


def test_replenishment_required(
    db_session,
    product,
    warehouse,
    demand_history
):
    from app.models.inventory import Inventory

    inventory = Inventory(
        warehouse_id=warehouse.warehouse_id,
        product_id=product.product_id,
        on_hand=200,
        reserved=100,
        on_order=100
    )

    db_session.add(inventory)
    db_session.commit()

    result = analyze_inventory(
        db_session,
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id
    )

    assert result["inventory_position"] == 200
    assert result["replenishment_required"] is True

    assert result["recommended_order_quantity"] == result["eoq"]