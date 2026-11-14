from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, DateTime, func, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.product import Product

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"),
                                        index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"),
                                        index=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_moment: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
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
        CheckConstraint("price_at_moment >= 0", name="check_price_at_moment_not_negative"),
        CheckConstraint("quantity > 0", name="check_quantity_positive")
    )

    UniqueConstraint("order_id", "product_id", name="unique_order_product")
    
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items", lazy="selectin")