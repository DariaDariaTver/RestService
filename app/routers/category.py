from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryRead
from sqlalchemy import select, func
from app.schemas.pagination import PaginationResponse
import math

router = APIRouter(prefix="/categories", tags=["categories"])

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