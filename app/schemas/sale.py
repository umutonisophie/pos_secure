from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class SaleBase(BaseModel):
    total_amount: Decimal
    customer_id: int | None = None
    user_id: int

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    total_amount: Decimal | None = None
    customer_id: int | None = None
    user_id: int | None = None

class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sale_date: datetime