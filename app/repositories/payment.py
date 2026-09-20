from models.payment import Payment
from sqlalchemy.orm import Session

class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get(self, db: Session, id: int):
        return db.get(Payment, id)

    def get_all(self, db: Session):
        payments = db.query(Payment).all()
        return payments

    def create(self, db: Session, data: dict):
        payment = Payment(**data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def update(self, db: Session, db_obj: Payment, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Payment):
        db.delete(db_obj)
        db.commit()
        return

payment_repository = PaymentRepository()