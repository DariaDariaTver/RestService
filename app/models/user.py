from sqlalchemy import Column, Integer, String, DateTime, Identity, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(always=True), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    pw_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, 
        server_default=func.now(),
        onupdate=func.now()
    )

    role = relationship("Role", back_populates="users")
    addresses = relationship("Address", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    orders = relationship(
        "Order",
        foreign_keys="Order.user_id",
        back_populates="user"
        )
    courier_orders = relationship(
        "Order",
        foreign_keys="Order.courier_id",
        back_populates="courier"
        )
    
