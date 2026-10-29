from fastapi import APIRouter, HTTPException, Depends, status, Response, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.schemas.pagination import PaginationResponse
from app.dependencies.auth import require_role
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
import math
from decimal import Decimal

router = APIRouter(prefix="/admin/products", tags=["admin_products"])

@router.get("/", response_model=PaginationResponse[ProductRead])
def list_products(
    category_id: int | None = None,
    search: str | None = None,
    only_available: bool = False,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)):
    stmt = select(Product)
    if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="min_price cannot be greater than max_price"
            )
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if only_available:
        stmt = stmt.where(Product.is_available.is_(True))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    sort_map = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price
    }
    sort_column = sort_map.get(sort_by, Product.id)
    if order == "desc":
        stmt = stmt.order_by(sort_column.desc(), Product.id.desc())
    else:
        stmt = stmt.order_by(sort_column.asc(), Product.id.asc())
    
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
def get_product(product_id: int,
                db: Session = Depends(get_db),
                admin: User = Depends(require_role("admin"))):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(
    data: ProductCreate,
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)):
    category = db.get(Category, data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found",
        )

    product = Product(
        name=data.name,
        description=data.description,
        composition=data.composition,
        price=data.price,
        weight=data.weight,
        image=data.image,
        is_available=data.is_available,
        category_id=data.category_id,
    )

    db.add(product)
    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exist",
        )
    return product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
    ):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
    ):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product.is_available = False
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)