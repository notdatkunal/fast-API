from sqlalchemy import Column, Boolean, String, Date, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import BASE
# student model
class Student(BASE):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20),nullable=True)
    age = Column(Integer)
    date_of_birth = Column(Date)
    blood_group = Column(String(10))
    address = Column(String(100),nullable=True)
    email = Column(String(50))
    phone_number = Column(String(10))

class Account(BASE):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey('institute.id'), nullable=True)
    transaction_date = Column(Date)
    transaction_type = Column(String(255))
    payment_mode = Column(String(255))
    particular_name = Column(String(255))
    transaction_amount_debit = Column(Float)
    transaction_amount_credit = Column(Float)
    description = Column(String(255))
    transaction_id = Column(String(255))
    payment_reference = Column(String(255))
    net_balance = Column(Float)

    # Define the bidirectional relationship
    institute = relationship('Institute', back_populates='accounts')

class Institute(BASE):
    __tablename__ = 'institute'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    pincode = Column(String(6), nullable=True)
    phone = Column(String(14), nullable=False)

    # Define the bidirectional relationship
    accounts = relationship('Account', back_populates='institute')
