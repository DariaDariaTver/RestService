from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductRead
from sqlalchemy import select

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductRead])
def list_products(
    category_id: int | None = None,
    search: str | None = None,
    only_available: bool = True,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    ):
    if category_id is None:
        stmt = select(Category).order_by(Category.sort).limit(1)
        first_category = db.scalars(stmt).first()
        if first_category:
            category_id = first_category.id
    if not category_id:
        return []
    stmt = select(Product).where(Product.category_id == category_id)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if only_available:
        stmt = stmt.where(Product.is_available == True)
    return db.scalars(stmt.offset(skip).limit(limit)).all()
            
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product or not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product