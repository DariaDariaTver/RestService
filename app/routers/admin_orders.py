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
from app.schemas.order import OrderCreate, OrderRead
from sqlalchemy.orm import Session, joinedload
from app.dependencies.auth import get_current_user, require_role
from app.database import get_db
from app.schemas.pagination import PaginationResponse
import math

router = APIRouter(prefix="/admin/orders", tags=["admin_orders"])

@router.get("/", response_model=PaginationResponse[OrderRead])
def get_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_id: int | None = None,
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)):
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

    