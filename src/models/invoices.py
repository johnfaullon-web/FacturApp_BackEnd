from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Boolean, func
from datetime import  datetime
from src.models import Base, session

class Invoices(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    total = Column(Float, default=0)
    completed = Column(Boolean, default=False)
    active = Column(Integer, default=1)
    
    def __init__(self, client_id, user_id):
        self.client_id = client_id
        self.user_id = user_id
        self.date = datetime.now()
        self.total = 0
        self.completed = False
        self.active = 1
        
    def __repr__(self):
        return f"<Invoice(id={self.id}, client_id={self.client_id}, user_id={self.user_id}, date='{self.date}', total={self.total}, completed={self.completed}, active={self.active})>"
    
    def get_paginated(page, per_page):
        total_invoices = session.query(func.count(Invoices.id)).scalar()
        invoices = session.query(Invoices).offset((page - 1) * per_page).limit(per_page).all()
        return invoices, total_invoices
    
    def get_by_id(invoice_id):
        invoice = session.query(Invoices).filter_by(id=invoice_id).first()
        return invoice
    
    def get_by_client_id(client_id):
        invoices = session.query(Invoices).filter_by(client_id=client_id).all()
        return invoices
    
    def save(self):
        session.add(self)
        session.commit()
        
    def update(self):
        session.commit()
