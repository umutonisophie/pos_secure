from fastapi import APIRouter
from schemas import SaleCreate, SaleRead, SaleUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import sale_service
from fastapi import Depends

router = APIRouter(prefix="/sales", tags=["sales"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    return sale_service.list_sale(db)

@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    return sale_service.get_sale(db, sale_id)

@router.post("/", response_model=SaleRead, status_code=201)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    return sale_service.create_sale(db, sale)


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: int, sale: SaleUpdate, db: Session = Depends(get_db)):
    return sale_service.update_sale(db, sale_id, sale)


@router.delete("/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    return sale_service.delete_sale(db, sale_id)