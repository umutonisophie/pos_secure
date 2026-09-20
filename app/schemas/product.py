from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    sku: str
    price: Decimal
    cost: Decimal | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    is_active: bool | None = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    price: Decimal | None = None
    cost: Decimal | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    is_active: bool | None = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime