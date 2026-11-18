from sqlalchemy import Column, Integer, Float, ForeignKey
from src.models import Base, session

class InvoiceDetails(Base):
    __tablename__ = 'invoice_details'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)

    def __init__(self, invoice_id, product_id, quantity, unit_price):
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def __repr__(self):
        return f"<InvoiceDetail(id={self.id}, invoice_id={self.invoice_id}, product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price})>"
    
    def get_by_id(detail_id):
        invoice_detail = session.query(InvoiceDetails).filter_by(id=detail_id).first()
        return invoice_detail

    def get_by_invoice(invoice_id):
        invoice_details = session.query(InvoiceDetails).filter_by(invoice_id=invoice_id).all()
        return invoice_details

    def get_by_invoice_and_product(invoice_id, product_id):
        invoice_detail = session.query(InvoiceDetails).filter_by(
            invoice_id=invoice_id,
            product_id=product_id
        ).first()
        return invoice_detail

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()