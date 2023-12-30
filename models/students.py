from database import BASE
from .base import *



class Student(BASE):
    __tablename__ = "tbl_students"
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(255), nullable=False)
    gender = Column(String(1000))
    date_of_birth = Column(Date)
    blood_group = Column(String(100))
    address = Column(Text(1000),nullable=True)
    phone_number = Column(String(100))
    email = Column(Text(5000))
    admission_date = Column(Date)
    roll_number = Column(String(255))
    photo = Column(BLOB,nullable=True)
    slug = Column(String(255),unique=True)

    # foreign keys
    class_id = Column(Integer,ForeignKey("tbl_classes.class_id",ondelete="CASCADE"),nullable=True)
    section_id = Column(Integer,ForeignKey("tbl_sections.section_id",ondelete="CASCADE"),nullable=True)
    transport_id = Column(Integer,ForeignKey("tbl_transport.transport_id",ondelete="CASCADE"),nullable=True)


class Parents(BASE):
    __tablename__ = "tbl_parents"
    parent_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_name = Column(String(255))
    parent_email = Column(String(255))
    parent_phone = Column(String(255))
    parent_profile = Column(Text(1000), nullable=True)
    parent_gender = Column(String(255), nullable=True)
    parent_age = Column(String(100),nullable=True)
    relation_with_student = Column(String(255))
    parent_address = Column(Text(5000),nullable=True)
    parent_profession = Column(String(255),nullable=True)
    photo = Column(BLOB(3000),nullable=True)

    # Foreign Keys
    student_id = Column(Integer,ForeignKey("tbl_students.student_id",ondelete="CASCADE"),nullable=True)