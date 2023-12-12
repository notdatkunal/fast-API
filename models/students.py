from database import BASE
from .base import *

class Student(BASE):
    __tablename__ = "students"
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(30), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    blood_group = Column(String(10))
    address = Column(String(100),nullable=True)
    phone_number = Column(String(10))
    email = Column(String(50))
    admission_date = Column(Date)
    roll_number = Column(String(20))
    photo = Column(String(255),nullable=True)
    slug = Column(String(255),unique=True)

    # foreign keys
    class_id = Column(Integer,ForeignKey("Tbl_Classes.class_id",ondelete="CASCADE"),nullable=True)
    section_id = Column(Integer,ForeignKey("Tbl_Sections.section_id",ondelete="CASCADE"),nullable=True)
    transport_id = Column(Integer,ForeignKey("Tbl_Transport.transport_id",ondelete="CASCADE"),nullable=True)

