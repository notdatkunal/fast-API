from database import BASE
from .base import *


class Classes(BASE):
    __tablename__ = "Tbl_Classes"
    class_id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    class_name = Column(String(10))
    is_deleted = Column(Boolean,default=False)
    slug = Column(String(100),unique=True)
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)



class Sections(BASE):
    __tablename__ = "Tbl_Sections"
    section_id = Column(Integer,primary_key=True,autoincrement=True)
    section_name = Column(String(10))
    class_id = Column(Integer,ForeignKey("Tbl_Classes.class_id",ondelete="CASCADE"))
    is_deleted = Column(Boolean,default=False)

class Subjects(BASE):
    __tablename__ = "Tbl_Subjects"
    subject_id = Column(Integer,primary_key=True,autoincrement=True)
    subject_name = Column(String(10))
    class_id = Column(Integer,ForeignKey("Tbl_Classes.class_id",ondelete="CASCADE"))
    is_deleted = Column(Boolean,default=False)