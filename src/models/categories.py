from sqlalchemy import Column, Integer, String, func
from src.models import Base, session


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    active = Column(Integer, default=1)  # 1 for active, 0 for inactive

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', description='{self.description}', active={self.active})>"

    def get_paginated(page, per_page):
        total_categories = session.query(func.count(Categories.id)).scalar()
        categories = session.query(Categories).offset((page - 1) * per_page).limit(per_page).all()
        return categories, total_categories

    def get_by_id(category_id):
        category = session.query(Categories).filter_by(id=category_id).first()
        return category

    def get_by_name(name):
        category = session.query(Categories).filter_by(name=name).first()
        return category

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()