from repositories import supplier_repository
from schemas.supplier import SupplierCreate, SupplierUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_supplier(db:Session, supplier_id:int):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier

def list_supplier(db: Session):
    return supplier_repository.get_all(db)

def create_supplier(db:Session, supplier:SupplierCreate):
    return supplier_repository.create(db, supplier.model_dump())

def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate):
    retrieved_supplier = get_supplier(db, supplier_id)
    updated_supplier = supplier_repository.update(db, retrieved_supplier, supplier.model_dump(exclude_unset=True))
    return updated_supplier

def delete_supplier(db: Session, supplier_id: int):
    deleted_supplier = get_supplier(db, supplier_id)
    try:
        return supplier_repository.delete(db, deleted_supplier)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Supplier {supplier_id}: it is still referenced by other records",
        )