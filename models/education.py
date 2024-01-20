from database import BASE
from .base import *

class EducationYear(BASE):
    __tablename__ = "tbl_education_year"
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)
    education_year_id = Column(Integer, primary_key=True, autoincrement=True)
    education_year_name = Column(String(255))
    education_year_start_date = Column(Date)
    education_year_end_date = Column(Date)
    is_active = Column(Boolean,default=False)
