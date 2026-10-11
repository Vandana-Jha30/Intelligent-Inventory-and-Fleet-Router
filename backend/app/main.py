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
from app.api.vehicle_routing import (
    router as vehicle_routing_router
)
from app.api.supply_chain import router as supply_chain_router
from app.api.transportation import (
    router as transportation_router
)
from app.api.facility_location import (
    router as facility_location_router
)
from app.api.min_cost_flow import router as min_cost_flow_router

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
app.include_router(vehicle_routing_router)
app.include_router(supply_chain_router)
app.include_router(transportation_router)
app.include_router(facility_location_router)
app.include_router(min_cost_flow_router)


@app.get("/")
def root():
    return {
        "message": "Intelligent Inventory and Fleet Router API is running"
    }