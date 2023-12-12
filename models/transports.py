from database import BASE
from .base import *

class Transport(BASE):
    __tablename__ = "Tbl_Transport"
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)
    transport_id = Column(Integer,primary_key=True,autoincrement=True)
    transport_name = Column(String(100),nullable=False)
    vehicle_number = Column(String(100))
    vehicle_details = Column(String(255),nullable=False)
    register_date = Column(Date)
    is_deleted = Column(Boolean,default=False)

class Stops(BASE):
    __tablename__ = "Tbl_Stops"
    stop_id = Column(Integer,primary_key=True,autoincrement=True)
    transport_id = Column(Integer,ForeignKey("Tbl_Transport.transport_id",ondelete="CASCADE"))
    stop_name = Column(String(20))