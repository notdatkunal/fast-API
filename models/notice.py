from database import BASE
from .base import *

class Notice(BASE):
    __tablename__ = 'Tbl_Notice'
    notice_id = Column(Integer, primary_key=True)
    institution_id = Column(Integer, ForeignKey('institute.id', ondelete="CASCADE"))
    notice_date = Column(Date)
    due_date = Column(Date)
    notice_title = Column(String(500))
    notice_description = Column(String(500))
    recipient = Column(String(50))
    notice_announced_by = Column(String(100))
    is_deleted = Column(Boolean, default=False)

class StudentNotice(Notice):
    __tablename__ = "student_notice"
    id = Column(Integer, ForeignKey("Tbl_Notice.notice_id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id",ondelete="CASCADE"))
    __mapper_args__ = {
        "polymorphic_identity": "student_notice",
    }

# craeteing staff notice
class StaffNotice(Notice):
    __tablename__ = "staff_notice"
    id = Column(Integer, ForeignKey("Tbl_Notice.notice_id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("tbl_staff.staff_id",ondelete="CASCADE"))
    __mapper_args__ = {
        "polymorphic_identity": "staff_notice",
    }
