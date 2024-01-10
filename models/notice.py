from database import BASE
from .base import *

class Notice(BASE):
    __tablename__ = 'tbl_notice'
    notice_id = Column(Integer, primary_key=True)
    institute_id = Column(Integer, ForeignKey('institute.id', ondelete="CASCADE"))
    notice_date = Column(Date)
    due_date = Column(Date)
    notice_title = Column(Text(5000))
    notice_description = Column(Text(5000))
    recipient = Column(Text(5000))
    notice_announced_by = Column(String(1000))
    is_deleted = Column(Boolean, default=False)

class StudentNotice(Notice):
    __tablename__ = "tbl_student_notice"
    id = Column(Integer, ForeignKey("tbl_notice.notice_id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("tbl_students.student_id",ondelete="SET NULL"))
    __mapper_args__ = {
        "polymorphic_identity": "student_notice",
    }

# craeteing staff notice
class StaffNotice(Notice):
    __tablename__ = "tbl_staff_notice"
    id = Column(Integer, ForeignKey("tbl_notice.notice_id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("tbl_staffs.staff_id",ondelete="SET NULL"))
    __mapper_args__ = {
        "polymorphic_identity": "staff_notice",
    }
