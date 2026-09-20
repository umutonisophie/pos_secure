from pydantic import BaseModel, ConfigDict

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int