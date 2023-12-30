from database import BASE
from .base import *

class Institute(BASE):
    __tablename__ = "institute"
    id = Column(Integer, primary_key=True, index=True)
    subscribers_id = Column(Integer, unique=True)
    institute_name = Column(String(500))
    institute_address = Column(String(500), nullable=True)
    institute_city = Column(String(500), nullable=True)
    institute_state = Column(String(500), nullable=True)
    institute_country = Column(String(500), nullable=True)
    institute_pincode = Column(String(500), nullable=True)
    institute_phone = Column(String(10))
    institute_email = Column(String(500), unique=True)
    institute_logo = Column(String(500), nullable=True)
    institute_fav_icon = Column(String(255), nullable=True)

    institute_tag_line = Column(String(255), nullable=True)

    institute_website = Column(String(255), nullable=True)

    point_of_contact = Column(String(255), nullable=True)

    date_of_registration = Column(Date, nullable=True)

    is_deleted = Column(Boolean, default=False)
