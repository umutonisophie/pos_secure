from fastapi import FastAPI
from routers import auth, product, category, customer, payment, receipt, sale, sale_item, supplier, user
from database import Base, engine
import models 


app = FastAPI(title="Point of Sale API", version="1")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(payment.router)
app.include_router(receipt.router)
app.include_router(sale.router)
app.include_router(sale_item.router)
app.include_router(supplier.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Point of Sale API"}