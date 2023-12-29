from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.notice import Notice,StudentNotice
from models.students import Student
from router.utility import succes_response
from pydantic import BaseModel

router = APIRouter()

# studentnotice
class StudentNoticeBase(BaseModel):
    student_roll_number:str
    notice_id:int



@router.post("/create_notice_per_student/")
async def create_notice_per_student(notice:StudentNoticeBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    notice = db.query(Notice).filter(Notice.notice_id == notice.notice_id).first()
    if notice is not None:
        raise HTTPException(status_code=404,detail="Notice not Found.")
    student_id = db.query(Student).filter(Student.roll_number == notice.student_roll_number).first()
    if student_id is not None:
        raise HTTPException(status_code=404,detail="Student not Found.")
    notice = StudentNotice()
    notice.notice_id = notice.notice_id
    notice.student_id = student_id.student_id
    db.add(notice)  
    db.commit()
    db.refresh(notice)
    return succes_response(jsonable_encoder(notice))
