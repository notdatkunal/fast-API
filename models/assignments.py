from database import BASE
from .base import *

class Assignments(BASE):
    __tablename__ = "tbl_assignments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True, name='institute_id')
    class_id = Column(Integer, ForeignKey("tbl_classes.class_id", ondelete="CASCADE"), nullable=True, name='class_id')
    section_id = Column(Integer, ForeignKey("tbl_sections.section_id", ondelete="CASCADE"), nullable=True, name='section_id')
    assignment_Date = Column(Date, nullable=False, name='assignment_date')
    assignment_title = Column(String(50), nullable=False, name='assignment_title')
    assignment_details = Column(String(100), nullable=False, name='assignment_details')
    assignment_due_date = Column(Date, nullable=False, name='assignment_due_date')
    is_deleted = Column(Boolean, default=False, name='is_deleted')


