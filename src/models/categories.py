from sqlalchemy import Column, Integer, String
from src.models import Base


class Categories(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    active = Column(Integer, nullable=True)