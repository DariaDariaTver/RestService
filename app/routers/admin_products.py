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

router = APIRouter(prefix="/admin/products", tags=["admin_products"])

@router.get("/", response_model=PaginationResponse[ProductRead])
def list_products(
    category_id: int | None = None,
    search: str | None = None,
    only_available: bool = True,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    ):
    stmt = select(Product)
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if only_available:
        stmt = stmt.where(Product.is_available == True)

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    product = db.scalars(stmt).all()
    pages = math.ceil(total / limit) if total > 0 else 0
    return {
            "items": product,
            "total": 0,
            "page": page,
            "pages": 0
            }
            
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
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
    db: Session = Depends(get_db),
):
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