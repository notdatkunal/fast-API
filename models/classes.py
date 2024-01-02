from database import BASE
from .base import *


class Classes(BASE):
    __tablename__ = "tbl_classes"
    class_id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    class_name = Column(String(1000))
    is_deleted = Column(Boolean,default=False)
    slug = Column(String(255),unique=True)
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)

    students = relationship("Student", back_populates="classes")
    assignments = relationship("Assignments", back_populates="classes")

class Sections(BASE):
    __tablename__ = "tbl_sections"
    section_id = Column(Integer,primary_key=True,autoincrement=True)
    section_name = Column(String(1000))
    class_id = Column(Integer,ForeignKey("tbl_classes.class_id",ondelete="CASCADE"))
    class_teacher = Column(Integer,ForeignKey("tbl_staffs.staff_id",ondelete="CASCADE"),nullable=True)
    is_deleted = Column(Boolean,default=False)

    students = relationship("Student", back_populates="sections")
    assignments = relationship("Assignments", back_populates="sections")

class Subjects(BASE):
    __tablename__ = "tbl_subjects"
    subject_id = Column(Integer,primary_key=True,autoincrement=True)
    subject_name = Column(String(1000))
    class_id = Column(Integer,ForeignKey("tbl_classes.class_id",ondelete="CASCADE"))
    is_deleted = Column(Boolean,default=False)