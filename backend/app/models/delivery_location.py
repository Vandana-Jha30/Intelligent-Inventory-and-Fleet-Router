from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class DeliveryLocation(Base):
    __tablename__ = "delivery_locations"

    location_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    location_name = Column(
        String,
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    demand_quantity = Column(
        Float,
        nullable=False
    )