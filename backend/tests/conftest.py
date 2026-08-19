import pytest

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app


from app.database.database import Base

from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.demand import DemandHistory


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        engine.dispose()


@pytest.fixture
def warehouse(db_session):
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

    return warehouse


@pytest.fixture
def product(db_session):
    product = Product(
        sku="TEST-001",
        name="Test Product",
        unit_cost=1500,
        ordering_cost=500,
        holding_cost=20,
        lead_time_days=5,
        service_level=0.95
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


@pytest.fixture
def inventory(db_session, warehouse, product):
    inventory = Inventory(
        warehouse_id=warehouse.warehouse_id,
        product_id=product.product_id,
        on_hand=450,
        reserved=100,
        on_order=300
    )

    db_session.add(inventory)
    db_session.commit()
    db_session.refresh(inventory)

    return inventory


@pytest.fixture
def demand_history(db_session, warehouse, product):
    demand_values = [95, 105, 98, 110, 102]

    records = []

    for index, quantity in enumerate(demand_values, start=1):
        demand = DemandHistory(
            product_id=product.product_id,
            warehouse_id=warehouse.warehouse_id,
            demand_date=date(2026, 8, index),
            quantity=quantity
        )

        db_session.add(demand)
        records.append(demand)

    db_session.commit()

    return records

@pytest.fixture
def client(db_session):
    from app.database.database import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()