from datetime import date
from enum import Enum
import sys
import uuid
sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.examination import ParentExam,Exam
from models.classes import Classes,Subjects
from models.institute import Institute
from router.utility import succes_response
from sqlalchemy.orm import joinedload,Load,load_only


router = APIRouter()

# parentBaseExam
class ParentBaseExam(BaseModel):
    parent_exam_name: str
    start_date: date
    end_date: date
    result_data: date
    class_id: int
    institute_id: int
    is_deleted: bool

    @validator('end_date')
    def end_date_validator(cls, v):
        if v < date.today():
            raise ValueError('End date must be greater than today')
        return v

    @validator('result_data')
    def result_data_validator(cls, v):
        if v < date.today():
            raise ValueError('Result date must be greater than today')
        return v 
    @validator('start_date')
    def start_date_validator(cls, v):
        if v < date.today():
            raise ValueError('Start date must be greater than today')
        return v


def check_intance_exist(id=None,model=None,db = None):
    model_ids = {
        Institute:"id",
        Classes:"class_id",
        Subjects:"subject_id",
    }
    if db.query(model).filter(getattr(model,model_ids[model]) == id).first() is None:
        return False
    return True

def genarete_parent_exam_slug(parent_exam_name=None,db=None):
    slug = parent_exam_name.replace(" ","-")
    while db.query(ParentExam).filter(ParentExam.parent_exam_slug == slug).first() is not None:
        slug = f"{slug}-{str(uuid.uuid4())[:6]}"
    return slug
# parentExam Post
@router.post("/create_parent_exam",description="Create Parent Exam")
async def create_parent_exam(parent_exam:ParentBaseExam,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if not check_intance_exist(id=parent_exam.institute_id,model=Institute,db=db):
        raise HTTPException(status_code=404, detail="Institute not found")
    if not check_intance_exist(id=parent_exam.class_id,model=Classes,db=db):
        raise HTTPException(status_code=404, detail="Class not found")
    try:
        new_parent_exam = ParentExam(**parent_exam.dict())
        new_parent_exam.parent_exam_slug = genarete_parent_exam_slug(parent_exam.parent_exam_name,db)
        db.add(new_parent_exam)
        db.commit()
        db.refresh(new_parent_exam)
        return succes_response(jsonable_encoder(new_parent_exam))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# get all parent exam by institute id
@router.get("/get_all_parent_exam_by_institute_id",description="Get All Parent Exam By Institute Id")
async def get_all_parent_exam_by_institute_id(institute_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if not check_intance_exist(id=institute_id,model=Institute,db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institute not found")
    try:
        parent_exam = (
            db.query(ParentExam)
            .join(Classes,ParentExam.class_id == Classes.class_id)
            .options(joinedload(ParentExam.classes).load_only(Classes.class_name))
            .filter(ParentExam.institute_id == institute_id)
            .order_by(ParentExam.start_date.desc())
            .all()
        )
        return jsonable_encoder(parent_exam)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")
    
# get parent exam by class id
@router.get("/get_parent_exam_by_class_id",description="Get Parent Exam By Class Id")
async def get_parent_exam_by_class_id(class_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if not check_intance_exist(id=class_id,model=Classes,db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    try:
        parent_exam = (
            db.query(ParentExam)
            .join(Classes,ParentExam.class_id == Classes.class_id)
            .options(joinedload(ParentExam.classes).load_only(Classes.class_name))
            .filter(ParentExam.class_id == class_id)
            .order_by(ParentExam.start_date.desc())
            .all()
        )
        return jsonable_encoder(parent_exam)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")

