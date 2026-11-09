from pydantic import Field, BaseModel, ConfigDict
from  decimal import Decimal
from app.schemas.product import ProductRead

class OrderCreate(BaseModel):
    address_id: int
    payment_method_id: int
    comment: str | None = None

class OrderItemRead(BaseModel):
    id: int
    quantity: int
    price_at_moment: Decimal
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    delivery_price: Decimal
    subtotal: Decimal
    total_price: Decimal
    status_id: int
    comment: str | None
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status_id: int