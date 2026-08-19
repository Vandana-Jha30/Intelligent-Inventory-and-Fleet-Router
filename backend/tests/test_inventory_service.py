import pytest
from pydantic import ValidationError

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate
from app.services.inventory_service import update_inventory

from app.services.inventory_service import (
    analyze_inventory,
    analyze_inventory_with_forecast
)


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


def test_analyze_inventory_with_forecast(
    db_session,
    product,
    warehouse,
    inventory,
    demand_history
):
    result = analyze_inventory_with_forecast(
        db=db_session,
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id,
        window=3
    )

    assert result["product_id"] == product.product_id
    assert result["warehouse_id"] == warehouse.warehouse_id

    assert result["forecast_daily_demand"] == pytest.approx(
         103.33333333333333
    )

    assert result["annual_demand"] == (
        result["forecast_daily_demand"] * 365
    )

    assert result["eoq"] > 0
    assert result["safety_stock"] > 0
    assert result["reorder_point"] > 0

def test_inventory_create_rejects_invalid_warehouse_id():
    with pytest.raises(ValidationError):
        InventoryCreate(
            warehouse_id=0,
            product_id=1,
            on_hand=10
        )


def test_inventory_create_rejects_invalid_product_id():
    with pytest.raises(ValidationError):
        InventoryCreate(
            warehouse_id=1,
            product_id=0,
            on_hand=10
        )


def test_inventory_create_rejects_negative_on_hand():
    with pytest.raises(ValidationError):
        InventoryCreate(
            warehouse_id=1,
            product_id=1,
            on_hand=-10
        )


def test_inventory_create_rejects_negative_reserved():
    with pytest.raises(ValidationError):
        InventoryCreate(
            warehouse_id=1,
            product_id=1,
            on_hand=10,
            reserved=-1
        )


def test_inventory_create_rejects_negative_on_order():
    with pytest.raises(ValidationError):
        InventoryCreate(
            warehouse_id=1,
            product_id=1,
            on_hand=10,
            on_order=-1
        )


def test_update_inventory_rejects_duplicate_warehouse_product(
    db_session
):
    inventory_1 = Inventory(
        warehouse_id=1,
        product_id=1,
        on_hand=100,
        reserved=0,
        on_order=0
    )

    inventory_2 = Inventory(
        warehouse_id=2,
        product_id=1,
        on_hand=200,
        reserved=0,
        on_order=0
    )

    db_session.add(inventory_1)
    db_session.add(inventory_2)
    db_session.commit()

    update_data = InventoryCreate(
        warehouse_id=1,
        product_id=1,
        on_hand=200,
        reserved=0,
        on_order=0
    )

    with pytest.raises(
        ValueError,
        match="Inventory already exists for this product and warehouse"
    ):
        update_inventory(
            db_session,
            inventory_2.inventory_id,
            update_data
        )