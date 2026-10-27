from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductRead
from sqlalchemy import select, func
from app.schemas.pagination import PaginationResponse
import math
from decimal import Decimal

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=PaginationResponse[ProductRead])
def list_products(
    category_id: int | None = None,
    search: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = Query(1, ge=1),
    only_available: bool = True,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    ):
    if category_id is None:
        stmt = select(Category).order_by(Category.sort).limit(1)
        first_category = db.scalars(stmt).first()
        if first_category:
            category_id = first_category.id
    if not category_id:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "pages": 0
        }
    
    stmt = select(Product).where(Product.category_id == category_id)

    if min_price is not None:
        stmt = stmt.where(Product.price >= min.price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max.price)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if only_available:
        stmt = stmt.where(Product.is_available == True)

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    sort_map = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price
    }
    sort_column = sort_map.get(sort_by, Product.id)
    if order == "desc":
        stmt = stmt.order_by(sort_column.desc())
    else:
        stmt = stmt.order_by(sort_column.asc())

    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    products = db.scalars(stmt).all()
    pages = math.ceil(total / limit) if total > 0 else 0
    return {
        "items": products,
        "total": total,
        "page": page,
        "pages": pages
    }
            
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product or not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product