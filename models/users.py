from database import BASE
from .base import *

class Users(BASE):
    __tablename__ = "users"
    # create fiels for user
    user_id = Column(Integer,primary_key=True,autoincrement=True)
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"))
    user_name = Column(String(20))
    user_phone_number = Column(String(10))
    user_email = Column(String(50))
    user_password = Column(String(100))
    user_role = Column(String(20))
    is_deleted = Column(Boolean,default=False)
    user_photo_url = Column(URLType)
