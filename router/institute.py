from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from router.utility import succes_response
from models.institute import Institute
router = APIRouter()
from models.users import Users
from .users.user import UserBase,get_password_hash


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


def create_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        new_user = Users(**user.dict())
        new_user.user_password = get_password_hash(new_user.user_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_user.user_password = user.user_password
        return succes_response(new_user)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/")
async def get_all_institutes(db: Session = Depends(get_db)):
    all_institutes = db.query(Institute).all()
    return jsonable_encoder(all_institutes)


@router.post("/")
async def create_institute(institute: InstituteBase, db: Session = Depends(get_db)):
    new_institute = Institute
    db.add(new_institute(**institute.__dict__))
    user_base = {
        "user_name": institute.point_of_contact,
        "user_password": institute.institute_phone,
        "user_email": institute.institute_email,
        "user_phone_number": institute.institute_phone,
        "user_role": "admin",
        "institute_id": int(institute.id),
        "is_deleted": False,
        'user_photo_url': "https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png"
    }
    create_user(UserBase(**user_base), db)
    db.commit()
    return {"msg": "Institute is Saved"}

@router.get("/Institute/")
async def get_institute_by_id(institute_id: int, db: Session = Depends(get_db)):
    try:
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if not institute:
            raise HTTPException(status_code=404, detail="Institute Not Found")
        return jsonable_encoder(institute)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Occured: {e}")



@router.put("/Institute/")
async def update_institute(institute_id:int,instituteBase: InstituteBase, db: Session = Depends(get_db)):
    try:
        institute = db.query(Institute).filter(Institute.id ==institute_id).first()
        if not institute:
            raise HTTPException(status_code=404, detail="Institute Not Found")
        institute = institute(**instituteBase.__dict__)
        db.commit()
        db.refresh(institute)
        return succes_response(institute)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Occured: {e}")

