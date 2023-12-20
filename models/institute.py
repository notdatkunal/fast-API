from sqlalchemy import Column, Boolean, String, Date, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import BASE

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