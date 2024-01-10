from database import BASE
from .base import *

class Activity(BASE):
    __tablename__ = 'tbl_activity'
    institution_id = Column(Integer, ForeignKey('institute.id',ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, primary_key=True,autoincrement=True)
    activity_name = Column(String(255))
    activity_description = Column(Text(5000),nullable=True)
    activity_date = Column(Date)
    activity_location = Column(String(255),nullable=True)
    is_deleted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('tbl_students.student_id', ondelete='SET NULL'), nullable=True)
    # relationship
    students = relationship('Student', back_populates='activity')
    
    def __repr__(self):
        return self.activity_name