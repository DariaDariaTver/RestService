from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Numeric, DateTime, ForeignKey, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.address import Address
    from app.models.payment_method import PaymentMethod
    from app.models.order_item import OrderItem
    from app.models.order_status import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    courier_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    delivery_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id", ondelete="RESTRICT"))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey(
        "payment_methods.id", ondelete="RESTRICT"))
    comment: Mapped[str | None] = mapped_column(Text)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("order_statuses.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False)
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="subtotal_not_negative"),
        CheckConstraint("delivery_price >= 0", name="delivery_price_not_negative"),
        CheckConstraint("total_price >= 0", name="total_price_not_negative"),)

    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="orders",
                                        lazy="selectin")
    courier: Mapped["User | None"] = relationship(foreign_keys=[courier_id],
                            back_populates="courier_orders")
    address: Mapped["Address"] = relationship(back_populates="orders")
    status: Mapped["OrderStatus"] = relationship(back_populates="orders")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order",
                                        lazy="selectin")
