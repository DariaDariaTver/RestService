from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class ProductBase(BaseModel):
    """Общие поля для схем Product."""
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    composition: str | None = None
    price: Decimal = Field(gt=0, decimal_places=2)
    weight: Decimal = Field(gt=0, decimal_places=2)
    image: str | None = Field(default=None, max_length=255)
    is_available: bool = True
    category_id: int

class ProductCreate(ProductBase):
    """Что приходит при создании."""
    pass

class ProductRead(ProductBase):
    """Что уходит."""
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    """Что приходит при обновлении."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    composition: str | None = None
    price: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    weight: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    image: str | None = Field(default=None, max_length=255)
    is_available: bool | None = None
    category_id: int | None = None