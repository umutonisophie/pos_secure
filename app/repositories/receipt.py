from models.receipt import Receipt
from sqlalchemy.orm import Session

class ReceiptRepository:
    def __init__(self):
        self.model = Receipt

    def get(self, db: Session, id: int):
        return db.get(Receipt, id)

    def get_all(self, db: Session):
        receipts = db.query(Receipt).all()
        return receipts

    def create(self, db: Session, data: dict):
        receipt = Receipt(**data)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt

    def update(self, db: Session, db_obj: Receipt, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Receipt):
        db.delete(db_obj)
        db.commit()
        return

receipt_repository = ReceiptRepository()