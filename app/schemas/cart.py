from pydantic import BaseModel, Field, ConfigDict
from app.schemas.product import ProductRead
from decimal import Decimal

class CartItemCreate(BaseModel):
    product_id: int 
    quantity: int = Field(gt=0)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemRead(BaseModel):
    id: int
    quantity: int
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)

class CartRead(BaseModel):
    items: list[CartItemRead]
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)
