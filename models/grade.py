from database import BASE
from .base import *
from sqlalchemy import Table

# Association Table
grades_classes_association = Table(
    'grades_classes_association',
    BASE.metadata,
    Column('grade_id', Integer, ForeignKey('tbl_grades.grade_id')),
    Column('class_id', Integer, ForeignKey('tbl_classes.class_id'))
)

class Grades(BASE):
    __tablename__ = "tbl_grades"
    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True)
    grade_name = Column(String(1000))
    percent_from = Column(BigInteger)
    percent_upto = Column(BigInteger)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    # classes = relationship("Classes", secondary=grades_classes_association, back_populates="grades")


