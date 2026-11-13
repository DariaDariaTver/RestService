from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.user import User
from app.schemas.order import OrderRead
from app.database import get_db
from app.dependencies.auth import require_role
from app.schemas.pagination import PaginationResponse
import math

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