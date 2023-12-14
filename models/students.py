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


class Parents(BASE):
    __tablename__ = "parents"
    parent_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_name = Column(String(30))
    parent_email = Column(String(30))
    parent_phone = Column(String(10))
    parent_profile = Column(String(10), nullable=True)
    parent_gender = Column(String(10), nullable=True)
    parent_age = Column(String(100),nullable=True)
    relation_with_student = Column(String(10))
    parent_address = Column(String(50),nullable=True)
    parent_profession = Column(String(20),nullable=True)
    photo = Column(String(255),nullable=True)

    # Foreign Keys
    student_id = Column(Integer,ForeignKey("students.student_id",ondelete="CASCADE"),nullable=True)