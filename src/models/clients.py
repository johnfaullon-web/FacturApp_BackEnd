from sqlalchemy import Column, Integer, String, func, Enum
from src.models import Base, session
import enum

class DocumentType(str, enum.Enum):
    CC = "CC"
    NIT = "NIT"
    CE = "CE"

class Clients(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    document_type = Column(Enum(DocumentType), nullable=False)
    document_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    active = Column(Integer, default=1)

    def __init__(self, name, email, phone, address, document_type, document_number):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.active = 1
        self.document_type = document_type
        self.document_number = document_number

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', address='{self.address}', active={self.active}, document_type='{self.document_type}', document_number='{self.document_number}')>"

    def get_paginated(page, per_page):
        total_clients = session.query(func.count(Clients.id)).scalar()
        clients = session.query(Clients).offset((page - 1) * per_page).limit(per_page).all()
        return clients, total_clients

    def get_by_id(client_id):
        client = session.query(Clients).filter_by(id=client_id).first()
        return client

    def get_by_document_number(document_number):
        client = session.query(Clients).filter_by(document_number=document_number).first()
        return client

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()   
 
    

