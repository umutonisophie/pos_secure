from models.sale import Sale
from sqlalchemy.orm import Session

class SaleRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, id: int):
        return db.get(Sale, id)

    def get_all(self, db: Session):
        sales = db.query(Sale).all()
        return sales

    def create(self, db: Session, data: dict):
        sale = Sale(**data)
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale

    def update(self, db: Session, db_obj: Sale, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale):
        db.delete(db_obj)
        db.commit()
        return

sale_repository = SaleRepository()