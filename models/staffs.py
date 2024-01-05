from database import BASE
from .base import *

class Staff(BASE):
    __tablename__ = "tbl_staffs"
    institute_id = Column(
        Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True
    )
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(255))
    staff_name = Column(String(255))
    photo = Column(Text(3000), nullable=True)
    role = Column(String(255), nullable=True)
    address = Column(Text(3000), nullable=True)
    gender = Column(String(255), nullable=True)
    experience = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)
    experience = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    blood_group = Column(String(255), nullable=True)
    date_of_birth = Column((Date), nullable=True)
    joining_date = Column((Date), nullable=True)
    salary = Column(String(255), nullable=True)
    slug = Column(String(255), unique=False)
    is_deleted = Column(Boolean, default=False)

    # foreign keys
    transport_id = Column(
        Integer,
        ForeignKey("tbl_transport.transport_id", ondelete="CASCADE"),
        nullable=True,
    )
    # relationships
    calender = relationship("Calender", back_populates="staffs")
    staff_attendance = relationship("StaffAttendance", back_populates="staff")

class Staff_Payroll(BASE):
    __tablename__ = "tbl_staff_payroll"
    payroll_id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_type = Column(String(1000), nullable=True)
    salary_amount = Column(String(1000), nullable=True)
    payment_date = Column((Date), nullable=True)
    payment_mode = Column(String(1000), nullable=True)
    payroll_details = Column(Text(5000), nullable=True)
    staff_id = Column(
        Integer, ForeignKey("tbl_staffs.staff_id", ondelete="CASCADE"), nullable=True
    )


class StaffDocuments(BASE):
    __tablename__ = "tbl_staff_documents"
    document_id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String(1000), nullable=True)
    document_file = Column(Text(5000), nullable=True)
    staff_id = Column(Integer, ForeignKey("tbl_staffs.staff_id", ondelete="CASCADE"), nullable=True)
    is_deleted = Column(Boolean, default=False)

