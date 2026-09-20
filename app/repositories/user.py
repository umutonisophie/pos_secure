from models.user import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    def get_by_username(self, db: Session, username: str):
            return db.query(User).filter(User.username == username).first()

    def get_all(self, db: Session):
        users = db.query(User).all()
        return users

    def create(self, db: Session, data: dict):
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User):
        db.delete(db_obj)
        db.commit()
        return

user_repository = UserRepository()