import jwt

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import create_access_token, decode_token, hash_password, verify_password
from repositories.user import user_repository
from schemas.user import UserCreate


def register(db: Session, user: UserCreate):
    if user_repository.get_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    values = user.model_dump()
    values["password_hash"] = hash_password(values.pop("password"))
    return user_repository.create(db, values)


def authenticate(db: Session, username: str, password: str):
    user = user_repository.get_by_username(db, username)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        subject = payload.get("sub")
        user_id = int(subject)
    except (TypeError, ValueError, KeyError, jwt.PyJWTError):
        raise credentials_exception

    user = user_repository.get(db, user_id)
    if not user:
        raise credentials_exception

    return user