from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.cart import Cart
    from app.models.address import Address
    from app.models.refresh_token import RefreshToken
    from app.models.order import Order

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    pw_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(),
        nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users", lazy="selectin")
    addresses: Mapped["Address"] = relationship(back_populates="user", lazy="select")
    cart: Mapped["Cart"] = relationship(back_populates="user", uselist=False, lazy="selectin")
    refresh_tokens: Mapped["RefreshToken"] = relationship(back_populates="user", lazy="select")
    orders: Mapped[list["Order"]] = relationship(back_populates="user",
        foreign_keys="Order.user_id")
    courier_orders: Mapped[list["Order"]] = relationship(back_populates="courier_orders",
        foreign_keys="Order.courier_id")