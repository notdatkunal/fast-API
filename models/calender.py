from database import BASE
from .base import *

class Calender(BASE):
    __tablename__ = "tbl_Calender"
    calender_id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer, ForeignKey("institute.id", ondelete="CASCADE"))
    class_id = Column(Integer, ForeignKey("tbl_classes.class_id", ondelete="CASCADE"))
    section_id = Column(Integer, ForeignKey("tbl_sections.section_id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("tbl_subjects.subject_id", ondelete="CASCADE"))
    staff_id = Column(Integer, ForeignKey("tbl_staffs.staff_id", ondelete="CASCADE"))
    
    day = Column(String(2000))
    start_time = Column(Time)
    end_time = Column(Time)

    # relationships
    classes = relationship("Classes", back_populates="calender")
    sections = relationship("Sections", back_populates="calender")
    subjects = relationship("Subjects", back_populates="calender")
    staffs = relationship("Staff", back_populates="calender")
    