from repositories import category_repository
from schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_category(db:Session, category_id:int):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


def list_category(db: Session):
    return category_repository.get_all(db)

def create_category(db:Session, category:CategoryCreate):
    return category_repository.create(db, category.model_dump())

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    retrieved_category = get_category(db, category_id)
    updated_category = category_repository.update(db, retrieved_category, category.model_dump(exclude_unset=True))
    return updated_category

def delete_category(db: Session, category_id: int):
    deleted_category = get_category(db, category_id)
    try:
        return category_repository.delete(db, deleted_category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete Category {category_id}: it is still referenced by other records",
        )