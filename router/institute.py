from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.institute import Institute
from router.utility import succes_response

router = APIRouter()

class InstituteBase(BaseModel):
    id: int
    subscribers_id: int
    institute_name: str
    institute_address: str = None
    institute_city: str = None
    institute_state: str = None
    institute_country: str = None
    institute_pincode: str = None
    institute_phone: str
    institute_email: str
    institute_logo: str = None
    institute_fav_icon: str = None
    institute_tag_line: str = None
    institute_website: str = None
    point_of_contact: str = None
    date_of_registration: date = Field(default_factory=date.today)
    is_deleted: bool = False

@router.get("/get_all_institutes/")
async def get_all_institutes(db:Session =Depends(get_db)):
    try:
        all_institutes = db.query(Institute).all()
        return jsonable_encoder(all_institutes)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.post("/create_institute/")
async def create_institute(institute:InstituteBase,db:Session = Depends(get_db)):
    try:
        new_institute = Institute(**institute.dict())
        db.add(new_institute)
        db.commit()
        db.refresh(new_institute)
        return succes_response(new_institute)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
