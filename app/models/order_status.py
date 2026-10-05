from sqlalchemy import Column, Identity, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="status")