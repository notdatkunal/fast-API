from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.users import Users
from router.utility import succes_response
from pydantic import BaseModel, Field
from .login import get_password_hash

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

class UpdateUser(BaseModel):
    user_name: str = Field(min_length=3, max_length=30)
    user_email: str = Field(min_length=3, max_length=30)
    user_phone_number: str = Field(min_length=10, max_length=10)
    user_role: str = Field(min_length=3, max_length=30)
    user_photo_url: str = Field(default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")

    
# create user
@router.post("/create_user/")
async def create_user(user:UserBase,db:Session = Depends(get_db)):
    try:
        new_user = Users(**user.dict())
        new_user.user_password = get_password_hash(new_user.user_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_user.user_password = user.user_password
        return succes_response(new_user,msg="User Created Successfully")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get_user_by_institute
@router.get("/get_users_by_institute/")
async def get_user_by_institute(institute_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        user = db.query(Users).filter(Users.institute_id == institute_id).all()
        return jsonable_encoder(user)
    except Exception as e:
        return HTTPException(status_code=404, detail=f"No ID Found")
    
# get_user_by_id
@router.get("/get_user_by_id/")
async def get_user_by_id(user_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        user = db.query(Users).filter(Users.user_id == user_id).first()
        return jsonable_encoder(user)
    except Exception as e:
        return HTTPException(status_code=404, detail=f"No ID Found")

# get_users_by_field
@router.get("/get_users_by_field/{field_name}/{field_value}/")
async def get_users_by_field(field_name:str,field_value:str,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    users_model = Users
    users_objs =ModelManager.get_data_by_field(db.query(users_model),field_name,field_value,users_model)
    return jsonable_encoder(users_objs)

# Update user route with authentication
@router.put("/update_user/")
async def update_user(user_id: int, user: UserBase, current_user: str = Depends(is_authenticated), db: Session = Depends(get_db)):
    user_data = db.query(Users).filter(Users.user_id == user_id).first()
    if user_data is not None:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(user_data, key, value)
        db.commit()
        db.refresh(user_data)    
        return succes_response(user_data,msg="User Updated Successfully")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

# patch method for updating user
@router.patch("/update_user_partial/")
async def update_user(user_id: int, current_user: str = Depends(is_authenticated), db: Session = Depends(get_db), user_data: dict = {}):
    user_instance = db.query(Users).filter(Users.user_id == user_id).first()
    if user_instance is not None:
        for key, value in user_data.items():
            setattr(user_instance, key, value)
        db.commit()
        db.refresh(user_instance)
        return succes_response(user_instance, msg="User Updated Successfully")
    else:
        raise HTTPException(status_code=404, detail="User not found")

    
@router.patch("/update_user_password/")
async def update_user_password(user_id: int, user_password: str, current_user: str = Depends(is_authenticated), db: Session = Depends(get_db)):
    user_data = db.query(Users).filter(Users.user_id == user_id).first()
    if user_data is not None:
        user_data.user_password = get_password_hash(user_password)
        db.commit()
        db.refresh(user_data)    
        return succes_response(user_data,msg="User Updated Successfully")
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Delete user route with authentication
@router.delete("/delete_user/")
async def delete_user(user_id: int, current_user: str = Depends(is_authenticated), db: Session = Depends(get_db)):
    user_data = db.query(Users).filter(Users.user_id == user_id).first()
    if user_data is not None:
        db.delete(user_data)
        db.commit()
        return succes_response(data="",msg="User Deleted Successfully")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    


    
