from repositories import sale_repository, user_repository, customer_repository
from schemas.sale import SaleCreate, SaleUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_sale(db: Session, sale_id: int):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale


def _validate_foreign_keys(db: Session, data: dict):
    user_id = data.get("user_id")
    if user_id is not None and not user_repository.get(db, user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

    customer_id = data.get("customer_id")
    if customer_id is not None and not customer_repository.get(db, customer_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Customer {customer_id} not found")


def list_sale(db: Session):
    return sale_repository.get_all(db)

def create_sale(db: Session, sale: SaleCreate):
    data = sale.model_dump()
    _validate_foreign_keys(db, data)
    return sale_repository.create(db, data)

def update_sale(db: Session, sale_id: int, sale: SaleUpdate):
    retrieved_sale = get_sale(db, sale_id)
    data = sale.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    updated_sale = sale_repository.update(db, retrieved_sale, data)
    return updated_sale

def delete_sale(db: Session, sale_id: int):
    deleted_sale = get_sale(db, sale_id)
    try:
        return sale_repository.delete(db, deleted_sale)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Sale {sale_id}: it is still referenced by other records",
        )