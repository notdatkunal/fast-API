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
    institute_address: str = Field("")
    institute_city: str = Field("")
    institute_state: str = Field("")
    institute_country: str = Field("")
    institute_pincode: str = Field("")
    institute_phone: str
    institute_email: str
    institute_logo: str = Field("")
    institute_fav_icon: str = Field("")
    institute_tag_line: str = Field("")
    institute_website: str = Field("")
    point_of_contact: str = Field("")
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

@router.get("/get_all_institutes/")
async def get_all_institutes(db:db_dependency,current_user: str = Depends(is_authenticated)):
    all_institutes = db.query(Institute).all()
    return jsonable_encoder(all_institutes)


@router.post("/")
async def create_institute(institute: InstituteBase, db:db_dependency):
    new_institute = Institute
    db.add(new_institute(**institute.__dict__))
    db.commit()
    return {"msg": "Institute is Saved"}

@router.get("/get_institute_by_id/")
async def get_institute_by_id(institute_id: int, db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if not institute:
            raise HTTPException(status_code=404, detail="Institute Not Found")
        return jsonable_encoder(institute)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Occured: {e}")

@router.put("/update_institute/")
async def update_institute(institute_id:int,instituteBase: InstituteBase, db:db_dependency,current_user: str = Depends(is_authenticated)):
    institute = db.query(Institute).filter(Institute.id ==institute_id).first()
    if institute is None:
        raise HTTPException(status_code=404, detail="Institute Not Found")
    else:
        for key, value in instituteBase.dict(exclude_unset=True).items():
            setattr(institute, key, value)
        db.commit()
        db.refresh(institute)
        return succes_response(institute,msg="Institute Updated Successfully")
    
@router.patch("/update_institute_partial/")
async def update_institute(institute_id: int,db: Session = Depends(get_db),current_user: str = Depends(is_authenticated),data: dict ={}):
    try:
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if institute is None:
            raise HTTPException(status_code=404, detail="Institute Not Found")
        for key, value in data.items():
            setattr(institute, key, value)
        db.commit()
        db.refresh(institute)
        return succes_response(institute, msg="Institute Updated Successfully")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

