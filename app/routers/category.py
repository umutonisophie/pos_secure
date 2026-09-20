from fastapi import APIRouter
from schemas import CategoryCreate, CategoryRead, CategoryUpdate
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from services import category_service
from fastapi import Depends

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return category_service.list_category(db)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(db, category_id, category)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)