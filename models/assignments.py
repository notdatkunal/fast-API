from database import BASE
from .base import *

class Assignments(BASE):
    __tablename__ = "tbl_assignments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True, name='institute_id')
    class_id = Column(Integer, ForeignKey("tbl_classes.class_id", ondelete="CASCADE"), nullable=True, name='class_id')
    section_id = Column(Integer, ForeignKey("tbl_sections.section_id", ondelete="CASCADE"), nullable=True, name='section_id')
    assignment_Date = Column(Date, nullable=False, name='assignment_date')
    assignment_title = Column(String(1000), nullable=False, name='assignment_title')
    assignment_details = Column(String(5000), nullable=False, name='assignment_details')
    assignment_due_date = Column(Date, nullable=False, name='assignment_due_date')
    is_deleted = Column(Boolean, default=False, name='is_deleted')
    
    classes = relationship("Classes", back_populates="assignments")
    sections = relationship("Sections", back_populates="assignments")
    assignment_submission = relationship("AssignmentSubmission", back_populates="assignments")


class AssignmentSubmission(BASE):
    __tablename__ = "tbl_assignment_submission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("tbl_assignments.id", ondelete="CASCADE"), nullable=True, name='assignment_id')
    student_id = Column(Integer, ForeignKey("tbl_students.student_id", ondelete="CASCADE"), nullable=True, name='student_id')
    submission_date = Column(Date, nullable=False, name='submission_date')
    submission_details = Column(Text(5000), nullable=False, name='submission_details')
    assignment_file = Column(String(1000), nullable=False, name='assignment_file')
    is_deleted = Column(Boolean, default=False, name='is_deleted')
    
    assignments = relationship("Assignments", back_populates="assignment_submission")
    students = relationship("Student", back_populates="assignment_submission")



