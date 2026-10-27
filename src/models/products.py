from sqlalchemy import Integer, String, Column 
from src.models import Base 

class Products(Base):
    __tablename__ = 'Products'
    
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String (255), nullable=False)
    description = Column(String (255), nullable=True)
    price =  Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    active = Column(Integer, nullable=True)
    