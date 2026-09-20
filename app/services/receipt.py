from repositories import receipt_repository, sale_repository
from schemas.receipt import ReceiptCreate, ReceiptUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_receipt(db: Session, receipt_id: int):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt


def _validate_foreign_keys(db: Session, data: dict):
    sale_id = data.get("sale_id")
    if sale_id is not None and not sale_repository.get(db, sale_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Sale {sale_id} not found")


def list_receipt(db: Session):
    return receipt_repository.get_all(db)

def create_receipt(db: Session, receipt: ReceiptCreate):
    data = receipt.model_dump()
    _validate_foreign_keys(db, data)
    try:
        return receipt_repository.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Receipt with number '{data.get('receipt_number')}' already exists",
        )

def update_receipt(db: Session, receipt_id: int, receipt: ReceiptUpdate):
    retrieved_receipt = get_receipt(db, receipt_id)
    data = receipt.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    try:
        updated_receipt = receipt_repository.update(db, retrieved_receipt, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Receipt with number '{data.get('receipt_number')}' already exists",
        )
    return updated_receipt

def delete_receipt(db: Session, receipt_id: int):
    deleted_receipt = get_receipt(db, receipt_id)
    try:
        return receipt_repository.delete(db, deleted_receipt)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Receipt {receipt_id}: it is still referenced by other records",
        )