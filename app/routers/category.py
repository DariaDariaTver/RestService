from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.dependencies.auth import require_role

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

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(data: CategoryCreate, admin: User = Depends(require_role("admin")),
                    db: Session = Depends(get_db)):
    """Создать категорию."""
    existing = db.query(Category).filter(Category.name == data.name).first()
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
    category = db.query(Category).filter(Category.id == category_id).first()
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

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, admin: User = Depends(require_role("admin")),
                    db: Session = Depends(get_db)):
    """Удалить категорию."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    db.delete(category)
    db.commit()