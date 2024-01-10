from database import BASE
from .base import *
from sqlalchemy import Table
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


# Define the association table
fees_installments_association = Table(
    'fees_installments_association',
    BASE.metadata,
    Column('fee_id', Integer, ForeignKey('tbl_fees.fee_id')),
    Column('installment_id', Integer, ForeignKey('tbl_class_installments.installment_id'))
)

class Fees(BASE):
    __tablename__ = 'tbl_fees'
    institution_id = Column(Integer, ForeignKey('institute.id',ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer,ForeignKey("tbl_classes.class_id",ondelete="SET NULL"))
    fee_id = Column(Integer, primary_key=True, autoincrement=True)
    fee_total = Column(DECIMAL(15, 2))
    fee_admission = Column(DECIMAL(15, 2))

    # Define the many-to-many relationship with ClassInstallment
    class_installments = relationship('ClassInstallment', secondary=fees_installments_association, back_populates='fees')
    class_fees = relationship("Classes",back_populates="fees")

class ClassInstallment(BASE):
    __tablename__ = 'tbl_class_installments'
    installment_id = Column(Integer, primary_key=True, autoincrement=True)
    installment_name = Column(String(255), nullable=True)
    installment_number = Column(Integer)

    # Define the many-to-many relationship with Fees
    fees = relationship('Fees', secondary=fees_installments_association, back_populates='class_installments')
