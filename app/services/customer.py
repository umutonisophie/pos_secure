from repositories import customer_repository
from schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_customer(db:Session, customer_id:int):
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def list_customer(db: Session):
    return customer_repository.get_all(db)

def create_customer(db:Session, customer:CustomerCreate):
    return customer_repository.create(db, customer.model_dump())

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    retrieved_customer = get_customer(db, customer_id)
    updated_customer = customer_repository.update(db, retrieved_customer, customer.model_dump(exclude_unset=True))
    return updated_customer

def delete_customer(db: Session, customer_id: int):
    deleted_customer = get_customer(db, customer_id)
    try:
        return customer_repository.delete(db, deleted_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Customer {customer_id}: it is still referenced by other records",
        )