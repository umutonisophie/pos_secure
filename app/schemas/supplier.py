from pydantic import BaseModel, ConfigDict

class SupplierBase(BaseModel):
    company_name: str
    contact_info: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    company_name: str | None = None
    contact_info: str | None = None

class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: int