from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.security import hash_password
from repositories import user_repository
from schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def list_user(db: Session):
    return user_repository.get_all(db)


def create_user(db: Session, user: UserCreate):
    if user_repository.get_by_username(db, user.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    values = user.model_dump()
    values["password_hash"] = hash_password(values.pop("password"))
    return user_repository.create(db, values)


def update_user(db: Session, user_id: int, user: UserUpdate):
    retrieved_user = get_user(db, user_id)
    values = user.model_dump(exclude_unset=True)

    if "password" in values:
        values["password_hash"] = hash_password(values.pop("password"))

    if "username" in values and values["username"] != retrieved_user.username:
        if user_repository.get_by_username(db, values["username"]):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    return user_repository.update(db, retrieved_user, values)


def delete_user(db: Session, user_id: int):
    deleted_user = get_user(db, user_id)
    try:
        return user_repository.delete(db, deleted_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete User {user_id}: it is still referenced by other records",
        )