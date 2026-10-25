from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.dependencies.auth import require_role
from sqlalchemy.exc import IntegrityError

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
        first_category = db.query(Category).order_by(Category.sort).first()
        if first_category:
            category_id = first_category.id
    if not category_id:
        return []
    query = db.query(Product).filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if only_available:
        query = query.filter(Product.is_available == True)
    return query.offset(skip).limit(limit).all()
            
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
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
    category = db.query(Category).filter(Category.id == data.category_id).first()
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
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
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
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product.is_available = False
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)