from repositories import product_repository, category_repository, supplier_repository
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_product(db: Session, product_id: int):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _validate_foreign_keys(db: Session, data: dict):
    category_id = data.get("category_id")
    if category_id is not None and not category_repository.get(db, category_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Category {category_id} not found")

    supplier_id = data.get("supplier_id")
    if supplier_id is not None and not supplier_repository.get(db, supplier_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Supplier {supplier_id} not found")


def list_product(db: Session):
    return product_repository.get_all(db)

def create_product(db: Session, product: ProductCreate):
    data = product.model_dump()
    _validate_foreign_keys(db, data)
    try:
        return product_repository.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Product with SKU '{data.get('sku')}' already exists",
        )

def update_product(db: Session, product_id: int, product: ProductUpdate):
    retrieved_product = get_product(db, product_id)
    data = product.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    try:
        updated_product = product_repository.update(db, retrieved_product, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Product with SKU '{data.get('sku')}' already exists",
        )
    return updated_product

def delete_product(db: Session, product_id: int):
    deleted_product = get_product(db, product_id)
    try:
        return product_repository.delete(db, deleted_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Product {product_id}: it is still referenced by other records",
        )