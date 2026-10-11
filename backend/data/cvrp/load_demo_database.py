import csv
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.demand import DemandHistory
from app.models.depot import Depot
from app.models.delivery_location import DeliveryLocation
from app.models.vehicle import Vehicle


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = "sqlite:///./iifr_cvrp_demo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def benchmark_to_coordinates(x, y):
    """
    Convert the benchmark's planar X/Y coordinates into
    synthetic latitude/longitude coordinates.

    The transformation preserves relative geometry for the
    integrated prototype but is NOT the original benchmark
    coordinate system.
    """
    latitude = 12.80 + (y * 0.01)
    longitude = 77.00 + (x * 0.01)

    return latitude, longitude


def load_customers(db):
    customer_file = BASE_DIR / "customers.csv"

    with open(customer_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            latitude, longitude = benchmark_to_coordinates(
                float(row["x"]),
                float(row["y"]),
            )

            customer = DeliveryLocation(
                location_id=int(row["location_id"]),
                location_name=row["location_name"],
                latitude=latitude,
                longitude=longitude,
                demand_quantity=float(row["demand"]),
            )

            db.add(customer)


def load_depot(db):
    depot_file = BASE_DIR / "depot.csv"

    with open(depot_file, newline="") as file:
        row = next(csv.DictReader(file))

    latitude, longitude = benchmark_to_coordinates(
        float(row["x"]),
        float(row["y"]),
    )

    depot = Depot(
        depot_id=int(row["depot_id"]),
        depot_name=row["depot_name"],
        latitude=latitude,
        longitude=longitude,
    )

    db.add(depot)


def load_product(db):
    product = Product(
        product_id=1,
        sku="IG-001",
        name="Industrial Gearbox",
        unit_cost=1000.0,
        ordering_cost=500.0,
        holding_cost=20.0,
        lead_time_days=7,
        service_level=0.95,
    )

    db.add(product)


def load_warehouses(db):
    warehouse_file = BASE_DIR / "warehouses.csv"

    with open(warehouse_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            latitude, longitude = benchmark_to_coordinates(
                float(row["x"]),
                float(row["y"]),
            )

            warehouse = Warehouse(
                warehouse_id=int(row["warehouse_id"]),
                name=row["name"],
                latitude=latitude,
                longitude=longitude,
                capacity=int(row["capacity"]),
                operating_cost=float(row["operating_cost"]),
            )

            db.add(warehouse)


def load_inventory(db):
    inventory_file = BASE_DIR / "inventory.csv"

    with open(inventory_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            inventory = Inventory(
                warehouse_id=int(row["warehouse_id"]),
                product_id=int(row["product_id"]),
                on_hand=int(row["on_hand"]),
                reserved=int(row["reserved"]),
                on_order=int(row["on_order"]),
            )

            db.add(inventory)


def load_vehicles(db):
    vehicle_file = BASE_DIR / "vehicles.csv"

    with open(vehicle_file, newline="") as file:
        reader = csv.DictReader(file)

        for index, row in enumerate(reader, start=1):
            vehicle = Vehicle(
                vehicle_id=index,
                vehicle_number=row["vehicle_number"],
                capacity=float(row["capacity"]),
                fixed_cost=float(row["fixed_cost"]),
                cost_per_km=float(row["cost_per_km"]),
            )

            db.add(vehicle)


def load_demand_history(db):
    """
    Synthetic historical demand used only by the inventory
    forecasting component.

    The CVRPLIB benchmark does not provide historical
    inventory demand.
    """

    demand_values = [
        35,
        38,
        40,
        42,
        39,
        41,
        37,
        43,
        40,
        42,
    ]

    start_date = date(2026, 1, 1)

    demand_id = 1

    for warehouse_id in [1, 2]:
        for index, quantity in enumerate(demand_values):
            demand = DemandHistory(
                demand_id=demand_id,
                product_id=1,
                warehouse_id=warehouse_id,
                demand_date=start_date + timedelta(days=index),
                quantity=quantity,
            )

            db.add(demand)
            demand_id += 1


def print_summary(db):
    products = db.query(Product).all()
    warehouses = db.query(Warehouse).all()
    inventory = db.query(Inventory).all()
    customers = db.query(DeliveryLocation).all()
    depots = db.query(Depot).all()
    vehicles = db.query(Vehicle).all()
    history = db.query(DemandHistory).all()

    total_demand = sum(
        customer.demand_quantity
        for customer in customers
    )

    total_available_inventory = sum(
        max(item.on_hand - item.reserved, 0)
        for item in inventory
    )

    total_vehicle_capacity = sum(
        vehicle.capacity
        for vehicle in vehicles
    )

    print("\n========== DEMO DATABASE ==========")
    print(f"Products:              {len(products)}")
    print(f"Warehouses:            {len(warehouses)}")
    print(f"Depots:                {len(depots)}")
    print(f"Customers:             {len(customers)}")
    print(f"Vehicles:              {len(vehicles)}")
    print(f"Demand history rows:   {len(history)}")
    print("-----------------------------------")
    print(f"Customer demand:       {total_demand}")
    print(f"Available inventory:   {total_available_inventory}")
    print(f"Vehicle capacity:      {total_vehicle_capacity}")
    print("-----------------------------------")
    print(
        f"Inventory surplus:     "
        f"{total_available_inventory - total_demand}"
    )
    print(
        f"Vehicle capacity left: "
        f"{total_vehicle_capacity - total_demand}"
    )
    print("===================================\n")


def main():
    database_file = Path("iifr_cvrp_demo.db")

    if database_file.exists():
        database_file.unlink()
        print("Removed existing demo database.")

    print("Creating demo database...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        load_product(db)
        load_warehouses(db)
        load_inventory(db)
        load_depot(db)
        load_customers(db)
        load_vehicles(db)
        load_demand_history(db)

        db.commit()

        print_summary(db)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()