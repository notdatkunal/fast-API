from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.users import Users
from router.utility import succes_response
from pydantic import BaseModel

router = APIRouter()
# base models
class UserBase(BaseModel):
    user_name: str = Field(min_length=3, max_length=30)
    user_password: str = Field(min_length=3, max_length=30)
    user_email: str = Field(min_length=3, max_length=30)
    user_phone_number: str = Field(min_length=10, max_length=10)
    is_deleted: bool = False
    user_role: str = Field(min_length=3, max_length=30)
    institute_id: int
    user_photo_url: str = Field(default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")

    
# create user
@router.post("/create_user/")
async def create_user(user:UserBase,db:Session = Depends(get_db)):
    try:
        new_user = Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return succes_response(new_user)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get_user_by_institute
@router.get("/get_users_by_institute/")
async def get_user_by_institute(institute_id:int,db:Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.institute_id == institute_id).all()
        return jsonable_encoder(user)
    except Exception as e:
        return HTTPException(status_code=404, detail=f"No ID Found")
    
# get_user_by_id
@router.get("/get_user_by_id/")
async def get_user_by_id(user_id:int,db:Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.user_id == user_id).first()
        return jsonable_encoder(user)
    except Exception as e:
        return HTTPException(status_code=404, detail=f"No ID Found")

# get_users_by_field
@router.get("/get_users_by_field/{field_name}/{field_value}/")
async def get_users_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    users_model = Users
    users_objs =ModelManager.get_data_by_field(db.query(users_model),field_name,field_value,users_model)
    return jsonable_encoder(users_objs)

# update_user
@router.put("/update_user/")
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)) :
    user_data=db.query(Users).filter(Users.user_id == user_id).first()
    if user_data is not None:
        for key ,value in user.dict(exclude_unset=True).items():
            setattr(user_data, key ,value)
        db.commit()
        db.refresh(user_data)    
        return succes_response(user_data)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# delete_user
@router.delete("/delete_user/")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_data = db.query(Users).filter(Users.user_id == user_id).first()
    if user_data is not None:
        user_data.is_deleted = True
        db.commit()
        db.refresh(user_data)
        return succes_response(user_data)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
