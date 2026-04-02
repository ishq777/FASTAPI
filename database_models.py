from sqlalchemy import Column, Float, Integer, String

from database import Base

class Product(Base): 

    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
