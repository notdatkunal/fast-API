from database import BASE
from .base import *

class Staff(BASE):
    __tablename__ = "tbl_staff"
    institute_id = Column(
        Integer, ForeignKey("institute.id", ondelete="CASCADE"), nullable=True
    )
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(20))
    staff_name = Column(String(30))
    photo = Column(String(255), nullable=True)
    role = Column(String(30), nullable=True)
    address = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    experience = Column(String(30), nullable=True)
    specialization = Column(String(30), nullable=True)
    experience = Column(String(30), nullable=True)
    phone_number = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    blood_group = Column(String(10), nullable=True)
    date_of_birth = Column((Date), nullable=True)
    joining_date = Column((Date), nullable=True)
    salary = Column(String(30), nullable=True)
    slug = Column(String(255), unique=False)
    is_deleted = Column(Boolean, default=False)

    # foreign keys
    transport_id = Column(
        Integer,
        ForeignKey("Tbl_Transport.transport_id", ondelete="CASCADE"),
        nullable=True,
    )

class Staff_Payroll(BASE):
    __tablename__ = "tbl_staff_payroll"
    payroll_id = Column(Integer, primary_key=True, autoincrement=True)
    payroll_type = Column(String(10), nullable=True)
    salary_amount = Column(String(10), nullable=True)
    payment_date = Column((Date), nullable=True)
    payment_mode = Column(String(10), nullable=True)
    payroll_details = Column(String(10), nullable=True)

    # foreign keys
    staff_id = Column(
        Integer, ForeignKey("tbl_staff.staff_id", ondelete="CASCADE"), nullable=True
    )
