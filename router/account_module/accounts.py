from datetime import date
from enum import Enum
import sys
sys.path.append("..")
from router.basic_import import *
from models.accounts import Accounts
from models.institute import Institute
from router.utility import succes_response
# Accounts.metadata.create_all(bind=engine)

router = APIRouter()

class TranctionBase(Enum):
    Debit = "Debit"
    Credit = "Credit"

class PaymentMode(Enum):
    Cash = "Cash"
    UPI = "UPI"
    Net_Banking_NEFT = "Net Banking-NEFT"
    Net_Banking_IMPS = "Net Banking-IMPS"
    Net_Banking_RTGS = "Net Banking-RTGS"
    Cheque = "Cheque"
    Demand_Draft = "Demand Draft"

class PaymentType(Enum):
    Salary = "Salary"
    Fee_Collections = "Fee Collections"
    Expenditure = "Expenditure"
    Other_Credits = "Other Credits"
    Other_Debits = "Other Debits"
    Adjustment = "Adjustment"

class AccountBase(BaseModel):
    institution_id: int
    date_of_entry: date = Field(default_factory=date.today)
    transaction_date: date = Field(default_factory=date.today)
    transaction_type: TranctionBase
    payment_mode: PaymentMode
    payment_type: PaymentType
    particular_name: str
    transaction_amount: float = Field(min_value=0)
    description: str
    transaction_id: str
    transaction_reference: str
    net_balance: float = Field(min_value=0)


# post method code
@router.post("/create_transaction/")
async def post_account_data(account:AccountBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        account_instance = Accounts(**account.dict())
        db.add(account_instance)
        db.commit()
        db.refresh(account_instance)
        return succes_response(account_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# featching all the data in the json formate
@router.get("/get_all_transaction_by_institute/")
async def get_all_tractions_by_institute(institute_id:int,db :Session = Depends(get_db)):
    institute_data = db.query(Institute).filter(Institute.id == institute_id).first()
    if institute_data is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    tranction_data = db.query(Accounts).filter(Accounts.institution_id == institute_id).all()
    if tranction_data is not None:
        return jsonable_encoder(tranction_data)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")

# geting perticular record 
@router.get("/get_transaction_by_id/")
async def get_transaction_by_id(account_id:int,db:Session = Depends(get_db)):
    account_data = db.query(Accounts).filter(Accounts.account_id == account_id).first()
    if account_data is not None:
        return succes_response(account_data)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")

@router.put("/adjust_transaction/")
async def adjust_transaction(account_id:int,account:AccountBase,db:Session = Depends(get_db)):
    institute_data = db.query(Institute).filter(Institute.id == account.institution_id).first()
    if institute_data is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    account_data = db.query(Accounts).filter(Accounts.account_id == account_id).first()
    if account_data is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    try:
        for key, value in account.dict(exclude_unset=True).items(): 
            setattr(account_data, key, value)
        db.commit()
        db.refresh(account_data)
        return succes_response(account_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete_transaction/")
async def delete_transaction(account_id:int,db:Session = Depends(get_db)):
    account_data = db.query(Accounts).filter(Accounts.account_id == account_id).first()
    if account_data is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(account_data)
    db.commit()
    return succes_response("Transaction Deleted Successfully")



