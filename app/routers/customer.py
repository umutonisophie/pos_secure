from fastapi import APIRouter
from schemas import CustomerCreate, CustomerRead, CustomerUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import customer_service
from fastapi import Depends

router = APIRouter(prefix="/customers", tags=["customers"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return customer_service.list_customer(db)

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.get_customer(db, customer_id)

@router.post("/", response_model=CustomerRead, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, customer)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    return customer_service.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.delete_customer(db, customer_id)