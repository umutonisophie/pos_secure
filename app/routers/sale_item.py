from fastapi import APIRouter
from schemas import SaleItemCreate, SaleItemRead, SaleItemUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import sale_item_service
from fastapi import Depends

router = APIRouter(prefix="/sale-items", tags=["sale-items"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[SaleItemRead])
def list_sale_items(db: Session = Depends(get_db)):
    return sale_item_service.list_sale_item(db)

@router.get("/{sale_item_id}", response_model=SaleItemRead)
def get_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    return sale_item_service.get_sale_item(db, sale_item_id)

@router.post("/", response_model=SaleItemRead, status_code=201)
def create_sale_item(sale_item: SaleItemCreate, db: Session = Depends(get_db)):
    return sale_item_service.create_sale_item(db, sale_item)


@router.put("/{sale_item_id}", response_model=SaleItemRead)
def update_sale_item(sale_item_id: int, sale_item: SaleItemUpdate, db: Session = Depends(get_db)):
    return sale_item_service.update_sale_item(db, sale_item_id, sale_item)


@router.delete("/{sale_item_id}", status_code=204)
def delete_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    return sale_item_service.delete_sale_item(db, sale_item_id)