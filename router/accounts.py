from datetime import date
import sys
sys.path.append("..")
# basic 
from .basic_import import *
# models
from models import *
transports.BASE.metadata.create_all(bind = engine)
router = APIRouter()

# creating basemodel for post method
class Account(BaseModel):
   transaction_date: date = Field(default_factory=date.today)
   transaction_type :str = Field(max_length=255)
   payment_mode :str = Field(max_length=255)
   particular_name :str = Field(max_length=255)
   transaction_amount_debit :Optional[float] 
   transaction_amount_credit : Optional[float]
   description : str = Field(max_length=255)
   transaction_id  : str = Field(max_length=255)
   payment_reference :  str = Field(max_length=255)
   net_balance : float =Field(gt=0)

# post method code
@router.post("/")
async def post_account_data(account:Account,db : SessionLocal = Depends(get_db)):
   account_instance = Account # asigning the Model
   db.add(account_instance(**account.__dict__,institute_id = 1)) # unpacking the dict 
   db.commit()  # don't forget to commit in Sql
   return jsonable_encoder(account)

# featching all the data in the json formate
@router.get("/")
async def get_all_acoounts_data(db: Session = Depends(get_db)):
   todo_model = db.query(Account).all()
   return jsonable_encoder(todo_model)

@router.get("/get_by_institute/{institute_id}")
async def get_by_institute(institute_id:int,db :Session = Depends(get_db)):
   if db.query(Institute).filter(Institute.id == institute_id).first():
      todo_model = db.query(Account).filter(Account.institute_id == institute_id).all()
      return jsonable_encoder(todo_model)
   return http_exception(404,'Institute Id is Not There')

# geting perticular record 
@router.get("/{account_id}")
async def read_item(account_id: int, db: Session = Depends(get_db)):
   account_data = db.query(Account).filter(Account.id == account_id).first()
   if account_data is not None: # checkinh the where valide is there or not
      return jsonable_encoder(account_data)
   else:
      return http_exception(404,'Data is not assoicated with id')

@router.put("/{account_id}")
async def update_account_data(account_id:int,account:Account,db:Session =Depends(get_db)):
   account_data = db.query(Account).filter(Account.id == account_id).first()
   if account_data is not None:
      # Update only the provided fields that are not None
      for key, value in account.dict(exclude_unset=True).items():
         setattr(account_data, key, value)
      db.commit()
      db.refresh(account_data)
      return {"status": 200, 'msg': "Change is Done", 'response': jsonable_encoder(account_data)}
   return http_exception(404,"Account not found")

@router.delete("/account_id}")
async def delete_account(account_id,db:SessionLocal=Depends(get_db)):
   account_data = db.query(Account).filter(Account.id==account_id).first()
   if  account_data is not None:
      db.delete(account_data)
      return {"status": 200, 'msg': "Change is Done"}
   return http_exception(404,"Account not found")

def http_exception(error_code,error_msg):
   raise HTTPException(status_code=error_code,detail=error_msg)



