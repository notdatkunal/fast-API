from database import BASE
from .base import *

class StudentAttendance(BASE):
    __tablename__ = "tbl_student_attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True, name='institute_id')
    student_id = Column(Integer, ForeignKey("tbl_students.student_id", ondelete="CASCADE"), nullable=True, name='student_id')
    attendance_date = Column(Date, nullable=False, name='attendance_date')
    attendance_status = Column(String(20), nullable=False, name='attendance_status')
    is_deleted = Column(Boolean, default=False, name='is_deleted')

    student = relationship("Student", back_populates="student_attendance")

class StaffAttendance(BASE):
    __tablename__ = "tbl_staff_attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True, name='institute_id')
    staff_id = Column(Integer, ForeignKey("tbl_staffs.staff_id", ondelete="CASCADE"), nullable=True, name='staff_id')
    attendance_date = Column(Date, nullable=False, name='attendance_date')
    attendance_status = Column(String(20), nullable=False, name='attendance_status')
    is_deleted = Column(Boolean, default=False, name='is_deleted')

    staff = relationship("Staff", back_populates="staff_attendance")