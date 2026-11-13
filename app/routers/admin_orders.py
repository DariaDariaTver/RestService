from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from decimal import Decimal
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.address import Address
from app.models.payment_method import PaymentMethod
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.order_status import OrderStatus
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate, OrderCourierUpdate
from sqlalchemy.orm import Session, joinedload
from app.dependencies.auth import get_current_user, require_role
from app.database import get_db
from app.schemas.pagination import PaginationResponse
import math
from typing import Annotated
from app.utils.order_transitions import ALLOWED_TRANSITIONS

router = APIRouter(prefix="/admin/orders", tags=["admin_orders"])

@router.get("/", response_model=PaginationResponse[OrderRead])
def get_orders(
    admin: Annotated[User, Depends(require_role("admin"))],
    db: Annotated[Session, Depends(get_db)],
    status_id: Annotated[int | None, Query()],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20):
    stmt = select(Order)
    if status_id:
        stmt = stmt.where(Order.status_id == status_id)
        
    total = db.scalar(select(func.count()).select_from(stmt.subquery))

    stmt = stmt.order_by(Order.created_at.desc())

    stmt = stmt.options(joinedload(Order.items).joinedload(OrderItem.product))
    
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    orders = db.scalars(stmt).unique().all()
    pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "items": orders,
        "total": total,
        "page": page,
        "pages": pages
    }

@router.patch("/{order_id}/status", response_model=OrderRead)
def update_status_order(
    order_id: int,
    data:  OrderStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(require_role("admin"))]):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    new_status = db.get(OrderStatus, data.status_id)
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New status not found"
        )
    current_status = db.get(OrderStatus, order.status_id)
    allowed = ALLOWED_TRANSITIONS.get(current_status.name, [])
    if new_status.name not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status transition"
        )
    order.status_id = data.status_id
    db.commit()
    db.refresh(order)
    
    return order

@router.patch("/{order_id}/courier",
            response_model=OrderRead)
def assign_courier(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(require_role("admin"))],
    order_id: int,
    data: OrderCourierUpdate):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found")
    courier = db.get(User, data.courier_id)
    if not courier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if courier.role.name != "courier":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not courier"
        )
    order.courier_id = courier.id
    db.commit()
    db.refresh(order)
    return order