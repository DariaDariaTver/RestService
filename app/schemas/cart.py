from pydantic import BaseModel, Field, ConfigDict
from app.schemas.product import ProductRead

class CartItemCreate(BaseModel):
    product_id: int 
    quantity: int = Field(ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)

class CartItemRead(BaseModel):
    id: int
    quantity: int
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)
