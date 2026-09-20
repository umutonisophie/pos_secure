from fastapi import APIRouter
from schemas import PaymentCreate, PaymentRead, PaymentUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import payment_service
from fastapi import Depends

router = APIRouter(prefix="/payments", tags=["payments"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db)):
    return payment_service.list_payment(db)

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)

@router.post("/", response_model=PaymentRead, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, payment)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_service.update_payment(db, payment_id, payment)


@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.delete_payment(db, payment_id)