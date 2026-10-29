from fastapi import APIRouter, HTTPException, Depends, status, Response, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.pagination import PaginationResponse
from app.dependencies.auth import require_role
from sqlalchemy import select, func
import math 

router = APIRouter(prefix="/admin/categories", tags=["admin_categories"])

@router.get("/", response_model=PaginationResponse[CategoryRead])
def list_categories(
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)):
    """Получить список категорий."""
    stmt = select(Category)
    if search:
        stmt = stmt.where(Category.name.ilike(f"%{search}%"))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.order_by(Category.sort, Category.id)
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    categories = db.scalars(stmt).all()
    pages = math.ceil(total / limit) if total > 0 else 0
    return {
        "items": categories,
        "total": total,
        "page": page,
        "pages": pages
    }

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(data: CategoryCreate, admin: User = Depends(require_role("admin")),
                    db: Session = Depends(get_db)):
    """Создать категорию."""
    stmt = select(Category).where(Category.name == data.name)
    existing = db.scalars(stmt).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name category already exist",
        )

    category = Category(
        name=data.name,
        description=data.description,
        sort=data.sort
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryUpdate,
                    admin: User = Depends(require_role("admin")),
                    db: Session = Depends(get_db)):
    """Обновить категорию."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    admin: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)):
    """Удалить категорию."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    stmt = select(Product).where(Product.category_id == category_id)
    product = db.scalars(stmt).first()
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with products",
        )
    
    db.delete(category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)