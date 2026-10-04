from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, String, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, Identity(always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city = Column(String(100), nullable=False)
    street = Column(String(150), nullable=False)
    house = Column(String(20), nullable=False)
    apartment = Column(String(20), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User",  back_populates="addresses")
    orders = relationship("Order", back_populates="address")
