from pydantic import BaseModel, Field, ConfigDict, computed_field
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

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return self.product.price * self.quantity
    
    model_config = ConfigDict(from_attributes=True)

class CartRead(BaseModel):
    items: list[CartItemRead]
    total_price: Decimal

    @computed_field
    @property
    def items_count(self) -> int:
        return sum(item.quantity for item in self.items)

    model_config = ConfigDict(from_attributes=True)
