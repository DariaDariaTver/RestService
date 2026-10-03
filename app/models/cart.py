from sqlalchemy import Column, Integer, Identity, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, Identity(always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    items = relationship("CartItem", back_populates="cart")
    user = relationship("User", back_populates="cart")
