from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.address import Address
from app.schemas.address import AddressRead, AddressCreate, UpdateAddress
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/", response_model=list[AddressRead])
def get_me_addreses(current_user: Annotated[User, Depends(get_current_user)],
                    db: Annotated[Session, Depends(get_db)]):
    stmt = select(Address).where(Address.user_id == current_user.id)
    return db.scalars(stmt).all()

@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(data: AddressCreate,
                   current_user: Annotated[User, Depends(get_current_user)],
                   db: Annotated[Session, Depends(get_db)]):
        try:
            new_address = Address(
                city=data.city,
                street=data.street,
                house=data.house,
                apartment=data.apartment,
                is_default=data.is_default,
                user_id=current_user.id )
            
            db.add(new_address)
            db.commit()
            db.refresh(new_address)
        except Exception as e:
            db.rollback()
            print(f"Ошибка создания адреса: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return new_address

@router.patch("/{address_id}", response_model=AddressRead)
def update_address(data: UpdateAddress,
                   address_id: int,
                   current_user: Annotated[User, Depends(get_current_user)],
                   db: Annotated[Session, Depends(get_db)]):
    address = db.get(Address, address_id)
    if not address or not address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address, key, value)

        db.commit()
        db.refresh(address)

        return address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int,
                   current_user: Annotated[User, Depends(get_current_user)],
                   db: Annotated[Session, Depends(get_db)]):
    address = db.get(Address, address_id)
    if not address or address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    db.delete(address)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)