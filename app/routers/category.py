from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    """Получить список категорий."""
    return(
    db.query(Category)
    .order_by(Category.sort, Category.id)
    .all()
    )

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category