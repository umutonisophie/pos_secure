from fastapi import APIRouter, Depends, HTTPException
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import product_service

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return product_service.list_product(db)

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_product(db, product_id, product)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)