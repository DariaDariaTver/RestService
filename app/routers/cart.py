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
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartRead)
def get_cart(current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db)):
    stmt = select(Cart)
    stmt = stmt.options(joinedload(Cart.items).joinedload(CartItem.product))
    stmt = stmt.where(Cart.user_id == current_user.id)
    cart = db.scalars(stmt).unique().first()
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
def add_cart_item(
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
    try:
        cart = db.scalars(
        select(Cart).where(Cart.user_id == current_user.id)).first()
        if cart is None:
            cart = Cart(user_id = current_user.id)
            db.add(cart)
            db.flush()

        existing_item = db.scalars(
        select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product.id)).first()
        if existing_item:
            existing_item.quantity += data.quantity
            item = existing_item
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=data.quantity,
            )
            db.add(item)
        db.commit()
        db.refresh(item)

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,
            detail="Operation conflicts"
        )
    return item
    
@router.patch("/items/{item_id}", response_model=CartItemRead)
def update_cart_item(
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
    
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
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
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    stmt = select(Cart).where(Cart.user_id == current_user.id)
    cart = db.scalars(stmt).first()
    if not cart:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    for item in cart.items:
        db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)