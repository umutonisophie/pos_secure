from fastapi import APIRouter
from schemas import ReceiptCreate, ReceiptRead, ReceiptUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import receipt_service
from fastapi import Depends

router = APIRouter(prefix="/receipts", tags=["receipts"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[ReceiptRead])
def list_receipts(db: Session = Depends(get_db)):
    return receipt_service.list_receipt(db)

@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return receipt_service.get_receipt(db, receipt_id)

@router.post("/", response_model=ReceiptRead, status_code=201)
def create_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db)):
    return receipt_service.create_receipt(db, receipt)


@router.put("/{receipt_id}", response_model=ReceiptRead)
def update_receipt(receipt_id: int, receipt: ReceiptUpdate, db: Session = Depends(get_db)):
    return receipt_service.update_receipt(db, receipt_id, receipt)


@router.delete("/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return receipt_service.delete_receipt(db, receipt_id)