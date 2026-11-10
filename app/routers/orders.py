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
from app.dependencies.auth import get_current_user
from app.database import get_db
from app.schemas.pagination import PaginationResponse
import math
from typing import Annotated

router = APIRouter(prefix="/orders", tags=["orders"])

DELIVERY_PRICE = Decimal("200.00")

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_router(data: OrderCreate,
                current_user: Annotated[User, Depends(get_current_user)],
                db: Annotated[Session, Depends(get_db)]):
    address = db.get(Address, data.address.id)
    if not address or address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    payment_method = db.get(PaymentMethod, data.payment_method.id)
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    order_status = db.scalars(select(OrderStatus).where(OrderStatus.name == "new")).first()
    if not order_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order status not found"
        )
    try:
        stmt = select(Cart).options(
            joinedload(Cart.items).joinedload(CartItem.product).where(
                Cart.user_id == current_user.id)
            )
        cart = db.scalars(stmt).first()
        if not cart or not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not items in cart"
            )
        for item in cart.items:
            if not item.product.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {item.product.name} is not available"
                )
            subtotal = Decimal("0.00")
            subtotal += item.product.price * item.quantity

            new_order = Order(
                user_id=current_user.id,
                status_id=order_status.id,
                address_id=address.id,
                payment_method_id=payment_method.id,
                comment=data.comment,
                subtotal=subtotal,
                delivery_price=DELIVERY_PRICE,
                total_price=subtotal + DELIVERY_PRICE,
            )
            db.add(new_order)
            db.flush()

            for item in cart.items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product.id,
                    price_at_moment=item.product.price,
                    quantity=item.quantity,
                )
                db.add(order_item)
                db.delete(item)

            db.commit()
            db.refresh(new_order)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error order create"
        )

@router.get("/", response_model=PaginationResponse[OrderRead])
def get_me_orders(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20):
    stmt = select(Order).where(Order.user_id == current_user.id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.order_by(Order.created_at.desc())
    stmt = stmt.options(joinedload(Order.items).joinedload(
        OrderItem.product))
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