from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.notice import Notice
from router.utility import succes_response
from sqlalchemy import Column,ForeignKey,Integer

router = APIRouter()
# base models
class NoticeBase(BaseModel):
    notice_date: date = Field(default_factory=date.today)
    due_date: date = Field(default_factory=date.today)
    notice_title: str
    notice_description: str
    recipient: str
    notice_announced_by: str
    is_deleted: bool = Field(default=False)
    institute_id:int
    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"))
    # create link from wher intitute id will come

# create notice
@router.post("/create_notice/")
async def create_notice(notice:NoticeBase,db:Session = Depends(get_db)):
    try:
        new_notice = Notice(**notice.dict())
        db.add(new_notice)
        db.commit()
        db.refresh(new_notice)
        return succes_response(jsonable_encoder(new_notice))
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# get_notices_institute_wise
@router.get("/get_notices_institute/")
async def get_notices_institute_wise(institute_id:int,db:Session = Depends(get_db)):
    notices = ModelManager.get_data_by_institute(db(Notice),Notice,institute_id)
    return jsonable_encoder(notices)

# get_notice_by_field
@router.get("/get_notice_by_field/{field_name}/{field_value}/")
async def get_notice_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    notice = ModelManager.get_data_by_field(db.query(Notice),field_name,field_value,Notice)
    return jsonable_encoder(notice)

# get_notice_by_id
@router.get("/get_notice_by_id/")
async def get_notice_by_id(notice_id:int,db:Session = Depends(get_db)):
    try:
        notice = db.query(Notice).filter(Notice.notice_id == notice_id).first()
        return jsonable_encoder(notice)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"No ID Found")
    
# update_notice
@router.put("/update_notice/")
async def update_notice(notice_id:int,notice:NoticeBase,db:Session = Depends(get_db)):
    try:
        notice_data = db.query(Notice).filter(Notice.notice_id == notice_id).first()
        if notice_data is not None:
            for key ,value in notice.dict(exclude_unset=True).items():
                setattr(notice_data, key ,value)
            db.commit()
            db.refresh(notice_data)    
            return succes_response(notice_data)
        else:
            raise HTTPException(status_code=404, detail="Notice not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Updating: {str(e)}")
    