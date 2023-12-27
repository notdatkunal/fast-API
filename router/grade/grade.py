from datetime import date,datetime,time
from enum import Enum
import sys
sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.grade import Grades
from router.utility import succes_response

router = APIRouter()
# gradebase model
class GradeBase(BaseModel):
    grade_name:str = Field(max_length=10,min_length=1)
    percent_from:int = Field(min_value=0,max_value=100)
    percent_upto :int = Field(min_value=1,max_value=100)
    is_deleted:bool = False
    @validator('percent_from')
    def percent_from_must_be_greater_than_percent_upto(cls, v, values, **kwargs):
        if 'percent_upto' in values and v > values['percent_upto']:
            raise ValueError('percent_from must be greater than percent_upto')
        return v
    
@router.post("/add_grade/")
async def add_grade(grade:GradeBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade_instance = Grades(**grade.dict())
        db.add(grade_instance)
        db.commit()
        db.refresh(grade_instance)
        return succes_response(grade_instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all_grade/")
async def get_all_grade(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grades = db.query(Grades).filter(Grades.is_deleted == False).order_by(Grades.grade_id.desc()).all()
        return jsonable_encoder(grades)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/get_grade_by_id/")
async def get_grade_by_id(grade_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade = db.query(Grades).filter(Grades.grade_id == grade_id and Grades.is_deleted == False).first()
        if grade is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        return succes_response(grade)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update_grade/")
async def update_grade(grade_id:int,grade:GradeBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade_instance = db.query(Grades).filter(Grades.grade_id == grade_id and Grades.is_deleted == False).first()
        if grade_instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        for var, value in vars(grade).items():
            setattr(grade_instance, var, value) if value else None
        db.commit()
        db.refresh(grade_instance)
        return succes_response(grade_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete_grade/")
async def delete_grade(grade_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade_instance = db.query(Grades).filter(Grades.grade_id == grade_id and Grades.is_deleted == False).first()
        if grade_instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        grade_instance.is_deleted = True
        db.commit()
        return succes_response("Grade deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))