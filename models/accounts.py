from database import BASE
from .base import *

class Accounts(BASE):
    __tablename__ = 'tbl_accounts'
    institution_id = Column(Integer, ForeignKey('institute.id',ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, primary_key=True,autoincrement=True)
    date_of_entry = Column(Date)
    transaction_date = Column(Date)
    transaction_type = Column(String(500))
    payment_mode = Column(String(500))
    payment_type = Column(String(500))
    particular_name = Column(String(255),nullable=True)
    description = Column(Text(5000), nullable=True)
    transaction_reference = Column(String(255),nullable=True)
    transaction_amount = Column(DECIMAL(15, 2))
    net_balance = Column(DECIMAL(15, 2))
