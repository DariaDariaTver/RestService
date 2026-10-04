from sqlalchemy import Column, Integer, String, DateTime, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="payment_method")