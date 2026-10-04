from sqlalchemy import Column, Integer, Numeric, Identity, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, Identity(always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    delivery_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    comment = Column(Text, nullable=True)
    status_id = Column(Integer, ForeignKey("order_statuses.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="orders")
    courier = relationship("User", foreign_keys=[courier_id], back_populates="courier_orders")
    address = relationship("Address", back_populates="orders")
    status = relationship("OrderStatus", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
