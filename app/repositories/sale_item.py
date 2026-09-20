from models.sale_item import SaleItem
from sqlalchemy.orm import Session

class SaleItemRepository:
    def __init__(self):
        self.model = SaleItem

    def get(self, db: Session, id: int):
        return db.get(SaleItem, id)

    def get_all(self, db: Session):
        sale_items = db.query(SaleItem).all()
        return sale_items

    def create(self, db: Session, data: dict):
        sale_item = SaleItem(**data)
        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)
        return sale_item

    def update(self, db: Session, db_obj: SaleItem, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SaleItem):
        db.delete(db_obj)
        db.commit()
        return

sale_item_repository = SaleItemRepository()