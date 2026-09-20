from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class PaymentBase(BaseModel):
    sale_id: int
    amount: Decimal
    payment_type: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    sale_id: int | None = None
    amount: Decimal | None = None
    payment_type: str | None = None

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int