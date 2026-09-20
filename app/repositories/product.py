from models.product import Product
from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, id: int):
        return db.get(Product, id)

    def get_all(self, db: Session):
        products = db.query(Product).all()
        return products

    def create(self, db: Session, data: dict):
        product = Product(**data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, db_obj: Product, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product):
        db.delete(db_obj)
        db.commit()
        return

product_repository = ProductRepository()