from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.user import User
from app.schemas.order import OrderRead, OrderStatusUpdate
from app.database import get_db
from app.dependencies.auth import require_role
from app.schemas.pagination import PaginationResponse
import math
from app.utils.order_transitions import ALLOWED_TRANSITIONS

router = APIRouter(prefix="/courier/orders", tags=["courier_orders"])

@router.get("/", response_model=PaginationResponse[OrderRead])
def get_curier_orders(
    current_user: Annotated[User, Depends(require_role("courier"))],
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20):
    stmt = select(Order).join(Order.status).where(
        Order.courier_id == current_user.id,
        OrderStatus.name.in_(["preparing", "delivering"]))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
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
    current_user: Annotated[User, Depends(require_role("courier"))],
    db: Annotated[Session, Depends(get_db)],
    order_id: int,
    data: OrderStatusUpdate):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.courier_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not your courier"
        )
    new_status = db.get(OrderStatus, data.status_id)
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not order status"
        )
    
    current_status = db.get(OrderStatus, order.status_id)
    allowed = ALLOWED_TRANSITIONS.get(
        current_status.name, [])
    if new_status.name not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    order.status_id = data.status_id
    db.commit()
    db.refresh(order)

    return order
