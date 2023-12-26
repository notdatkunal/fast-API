from database import BASE
from .base import *

class Transport(BASE):
    __tablename__ = "tbl_transport"
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)
    transport_id = Column(Integer,primary_key=True,autoincrement=True)
    transport_name = Column(String(100),nullable=False)
    vehicle_number = Column(String(100))
    vehicle_details = Column(String(255),nullable=False)
    register_date = Column(Date)
    is_deleted = Column(Boolean,default=False)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True, name='institute_id')

class Stops(BASE):
    __tablename__ = "tbl_stops"
    stop_id = Column(Integer,primary_key=True,autoincrement=True)
    transport_id = Column(Integer,ForeignKey("tbl_transport.transport_id",ondelete="CASCADE"))
    stop_name = Column(String(20)) 

class TransportRoute(BASE):
    __tablename__ = "tbl_transport_route"
    id = Column(Integer,primary_key=True,autoincrement=True)