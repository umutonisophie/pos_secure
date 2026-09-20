from repositories import sale_item_repository, sale_repository, product_repository
from schemas.sale_item import SaleItemCreate, SaleItemUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_sale_item(db: Session, sale_item_id: int):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Sale item not found")
    return sale_item


def _validate_foreign_keys(db: Session, data: dict):
    sale_id = data.get("sale_id")
    if sale_id is not None and not sale_repository.get(db, sale_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Sale {sale_id} not found")

    product_id = data.get("product_id")
    if product_id is not None and not product_repository.get(db, product_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found")


def list_sale_item(db: Session):
    return sale_item_repository.get_all(db)

def create_sale_item(db: Session, sale_item: SaleItemCreate):
    data = sale_item.model_dump()
    _validate_foreign_keys(db, data)
    return sale_item_repository.create(db, data)

def update_sale_item(db: Session, sale_item_id: int, sale_item: SaleItemUpdate):
    retrieved_sale_item = get_sale_item(db, sale_item_id)
    data = sale_item.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    updated_sale_item = sale_item_repository.update(db, retrieved_sale_item, data)
    return updated_sale_item

def delete_sale_item(db: Session, sale_item_id: int):
    deleted_sale_item = get_sale_item(db, sale_item_id)
    try:
        return sale_item_repository.delete(db, deleted_sale_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete SaleItem {sale_item_id}: it is still referenced by other records",
        )