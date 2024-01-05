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

# ExamBase
class ExamBase(BaseModel):
    parent_exam_id : int
    subject_id :int
    full_marks :int = Field(min_value=1,max_value=100)
    is_deleted : bool = False


# base function 
def get_exam_by_filter(db = None,filter_column=None,filter_value=None):
    try:
        exam_data = (
            db.query(Exam)
            .join(ParentExam,Exam.parent_exam_id == ParentExam.parent_exam_id)
            .join(Subjects,Exam.subject_id == Subjects.subject_id)
            .options(
                joinedload(Exam.parent_exam).load_only(ParentExam.parent_exam_name),
                joinedload(Exam.subject).load_only(Subjects.subject_name)
            )
            .filter(getattr(Exam,filter_column) == filter_value and Exam.is_deleted == False)
            .order_by(Exam.exam_id.desc())
            .all()
        )
        return jsonable_encoder(exam_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# create exam
@router.post("/create_exam/")
async def create_exam(exam:ExamBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if db.query(ParentExam).filter(ParentExam.parent_exam_id == exam.parent_exam_id).first() is None:
            raise HTTPException(status_code=404, detail="Parent exam not found")

    if db.query(Subjects).filter(Subjects.subject_id == exam.subject_id).first() is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    try:
        exam_instance = Exam(**exam.dict())
        db.add(exam_instance)
        db.commit()
        db.refresh(exam_instance)
        exam_instance = get_exam_by_filter(db,"exam_id",exam_instance.exam_id)
        return succes_response(exam_instance)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# get exam by parent exam id
@router.get("/get_exam_by_parent_exam_id/")
async def get_exam_by_parent_exam_id(parent_exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    exam = get_exam_by_filter(db,"parent_exam_id",parent_exam_id)
    return succes_response(exam)

# get exam by exam id
@router.get("/get_exam_by_exam_id/")
async def get_exam_by_exam_id(exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    exam = get_exam_by_filter(db,"exam_id",exam_id)
    return succes_response(exam)

# update exam
@router.put("/update_exam/")
async def update_exam(exam_id:int,exam:ExamBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if db.query(ParentExam).filter(ParentExam.parent_exam_id == exam.parent_exam_id).first() is None:
            raise HTTPException(status_code=404, detail="Parent exam not found")

    if db.query(Subjects).filter(Subjects.subject_id == exam.subject_id).first() is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    exam_instance = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if exam_instance is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    try:
        exam_instance.parent_exam_id = exam.parent_exam_id
        exam_instance.subject_id = exam.subject_id
        exam_instance.full_marks = exam.full_marks
        db.commit()
        db.refresh(exam_instance)
        exam_instance = get_exam_by_filter(db,"exam_id",exam_instance.exam_id)
        return succes_response(exam_instance)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# delete exam
@router.delete("/delete_exam/")
async def delete_exam(exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    exam_instance = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if exam_instance is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    try:
        db.delete(exam_instance)
        db.commit()
        return succes_response("Exam Deleted Successfully")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

