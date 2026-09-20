

from sqlalchemy import(
    Column,
    Integer,
    String
)
from database import Base

from sqlalchemy.orm import relationship
class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,index=True)    
    name=Column(String,nullable=False)                 
    description=Column(String,nullable=True)          
    products=relationship("Product",back_populates="category") 

