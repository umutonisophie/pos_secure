from fastapi import APIRouter
from schemas import SupplierCreate, SupplierRead, SupplierUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import supplier_service
from fastapi import Depends

router = APIRouter(prefix="/suppliers", tags=["suppliers"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    return supplier_service.list_supplier(db)

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return supplier_service.get_supplier(db, supplier_id)

@router.post("/", response_model=SupplierRead, status_code=201)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return supplier_service.create_supplier(db, supplier)


@router.put("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    return supplier_service.update_supplier(db, supplier_id, supplier)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return supplier_service.delete_supplier(db, supplier_id)