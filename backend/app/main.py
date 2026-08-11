from fastapi import FastAPI

from app.database.database import engine, Base
from app.models.warehouse import Warehouse
from app.api.warehouses import router as warehouse_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Intelligent Inventory and Fleet Router",
    description="Operations Research based Supply Chain Optimization Platform",
    version="1.0.0"
)


app.include_router(warehouse_router)


@app.get("/")
def root():
    return {
        "message": "Intelligent Inventory and Fleet Router API is running"
    }