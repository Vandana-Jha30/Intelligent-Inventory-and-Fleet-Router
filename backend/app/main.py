from fastapi import FastAPI

from app.database.database import engine, Base
from app.models.warehouse import Warehouse
from app.api.warehouses import router as warehouse_router
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.demand import DemandHistory
from app.api.products import router as product_router
from app.api.demand import router as demand_router
from app.api.inventory import router as inventory_router
from app.models.vehicle import Vehicle
from app.api.vehicles import router as vehicle_router
from app.models.delivery_location import DeliveryLocation
from app.api.delivery_locations import router as delivery_location_router
from app.models.depot import Depot
from app.api.depots import router as depot_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Intelligent Inventory and Fleet Router",
    description="Operations Research based Supply Chain Optimization Platform",
    version="1.0.0"
)


app.include_router(warehouse_router)
app.include_router(product_router)
app.include_router(demand_router)
app.include_router(inventory_router)
app.include_router(vehicle_router)
app.include_router(delivery_location_router)
app.include_router(depot_router)


@app.get("/")
def root():
    return {
        "message": "Intelligent Inventory and Fleet Router API is running"
    }