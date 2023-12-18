from database import BASE
from .base import *

class Assignments(BASE):
    __tablename__ = 'Tbl_Assignment'
    assignment_id = Column(Integer, primary_key=True,index=True)
    institution_id = Column(Integer, ForeignKey('institute.id'))
    assignment_Date = Column(Date)
    assignment_title = Column(String(100))
    assignment_details = Column(String(500))
    assignment_due_date = Column(Date)
    section_id = Column(Integer, ForeignKey('Tbl_Sections.section_id',ondelete="CASCADE"))
    class_id = Column(Integer, ForeignKey('Tbl_Classes.class_id ',ondelete="CASCADE"))
    is_delete = Column(Boolean,default=False)

