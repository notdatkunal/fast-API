from database import BASE
from .base import *

class Grades(BASE):
    __tablename__ = "tbl_grades"
    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    grade_name = Column(String(50))
    percent_from = Column(BigInteger)
    percent_upto = Column(BigInteger)
    is_deleted = Column(Boolean, default=False)

class GradeApplicable(BASE):
    __tablename__ = "tbl_grade_applicable"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"),nullable=True)
    grade_id = Column(Integer, ForeignKey("tbl_grades.grade_id", ondelete="CASCADE"),nullable=True)
    class_id = Column(Integer, ForeignKey("tbl_classes.class_id", ondelete="CASCADE"),nullable=True)
    is_deleted = Column(Boolean, default=False)

