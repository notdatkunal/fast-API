import sys
sys.path.append("..")
# basic 
from .basic_import import *
# models
from models import *
router = APIRouter()

class InstituteSchema(BaseModel):
    name :str = Field(max_length=20)
    address :Optional[str]
    city :Optional[str]
    state :Optional[str]
    country :Optional[str]
    pincode :Optional[str]
    phone :str = Field(max_length=10,min_length=10)
@router.get("/")
async def get_all_institutes(db:Session =Depends(get_db)):
    all_institutes = db.query(Institute).all()
    return jsonable_encoder(all_institutes)

@router.post("/")
async def create_institute(institute:InstituteSchema,db:Session = Depends(get_db)):
    new_institute = Institute
    db.add(new_institute(**institute.__dict__))
    db.commit()
    return {"msg":"Institute is Saved"}
