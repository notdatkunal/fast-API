from database import BASE
from .base import *

class ParentExam(BASE):
    __tablename__ = "tbl_parent_exams"
    parent_exam_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_exam_name = Column(Text)  
    start_date = Column(Date)
    end_date = Column(Date)
    result_data = Column(Date)
    parent_exam_slug = Column(String(500), unique=True) 
    class_id = Column(Integer, ForeignKey("tbl_classes.class_id", ondelete="CASCADE"), nullable=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True)
    is_deleted = Column(Boolean, default=False)

    classes = relationship("Classes", back_populates="parent_exam")



class Exam(BASE):
    __tablename__ = "tbl_exams"
    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_exam_id = Column(Integer, ForeignKey("tbl_parent_exams.parent_exam_id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("tbl_subjects.subject_id", ondelete="CASCADE"))
    full_marks = Column(Integer)
    pass_marks = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    subject = relationship("Subjects", back_populates="exam")
