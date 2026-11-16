from pydantic import BaseModel, ConfigDict

class AddressBase(BaseModel):
    city: str
    street: str
    house: str
    apartment: str | None = None
    is_default: bool = False

class AddressRead(AddressBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class AddressCreate(AddressBase):
    pass

class UpdateAddress(BaseModel):
    city: str | None = None
    street: str | None = None
    house: str | None = None
    apartment: str | None = None
    is_default: bool | None = None