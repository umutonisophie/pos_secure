from repositories import payment_repository, sale_repository
from schemas.payment import PaymentCreate, PaymentUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_payment(db: Session, payment_id: int):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


def _validate_foreign_keys(db: Session, data: dict):
    sale_id = data.get("sale_id")
    if sale_id is not None and not sale_repository.get(db, sale_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Sale {sale_id} not found")


def list_payment(db: Session):
    return payment_repository.get_all(db)

def create_payment(db: Session, payment: PaymentCreate):
    data = payment.model_dump()
    _validate_foreign_keys(db, data)
    return payment_repository.create(db, data)

def update_payment(db: Session, payment_id: int, payment: PaymentUpdate):
    retrieved_payment = get_payment(db, payment_id)
    data = payment.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    updated_payment = payment_repository.update(db, retrieved_payment, data)
    return updated_payment

def delete_payment(db: Session, payment_id: int):
    deleted_payment = get_payment(db, payment_id)
    try:
        return payment_repository.delete(db, deleted_payment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Payment {payment_id}: it is still referenced by other records",
        )