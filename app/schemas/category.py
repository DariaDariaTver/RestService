from pydantic import BaseModel, Field, ConfigDict

class CategoryBase(BaseModel):
    """Общие поля для категории."""
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    sort: int = 0
    is_visible: bool = True

class CategoryCreate(CategoryBase):
    """Что приходит при создании категории."""
    pass

class CategoryRead(CategoryBase):
    """Что уходит."""
    id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    """Что приходит при обновлении."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    sort: int | None = None
    is_visible: bool | None = None
