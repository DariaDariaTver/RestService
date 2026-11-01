from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal
from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.schemas.cart import CartItemRead, CartRead, CartItemCreate, CartItemUpdate
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartRead)
def get_cart(current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db)):
    stmt = select(Cart)
    stmt = stmt.options(
        joinedload(Cart.items).joineload(CartItem.product))
    stmt = stmt.where(Cart.user.id == current_user.id)
    cart = db.scalars(stmt).first()
    if cart is None:
        return {
            "items": [],
            "total_price": Decimal("0.00")
        }
    total_price = Decimal("0.00")
    for item in cart.items:
        total_price += item.product.price * item.quantity
    return {
        "items": cart.items,
        "total_price": total_price
        }

@router.post("/items", response_model=CartItemRead, status_code=201)
def create_cart(
    data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    product = db.get(Product, data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available"
        )
    stmt = select(Cart).where(Cart.user_id == current_user.id)
    cart = db.scalars(stmt).first()
    if not cart:
        cart = Cart(user_id = current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

        stmt = select(CartItem)
        stmt = stmt.where(CartItem.cart_id == cart.id)
        stmt = stmt.where(CartItem.product_id == product.id)
        existing_item = db.scalars(stmt).first()
        if existing_item:
                existing_item.quantity = existing_item.quantity + data.quantity
                db.commit()
                db.refresh(existing_item)
                return existing_item
        new_item = CartItem(
        cart_id=cart.id,
        product_id=product.id,
        quantity=data.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@router.patch("/items/{item_id}", response_model=CartItemRead)
def update_cart(
    item_id: int,
    data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    item = db.get(CartItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    if item.cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    if data.quantity == 0:
        db.delete(item)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item