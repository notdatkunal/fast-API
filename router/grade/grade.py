from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.grade import Grades
from models import Classes
from router.utility import succes_response

router = APIRouter()

# base models
class GradeBase(BaseModel):
    institute_id:int
    class_id:int
    grade_name:str = Field(min_length=1)
    percent_from: int
    percent_upto: int
    is_deleted: bool = False

# basic grade
def get_grade_by_filter(db=None,filter_column:str=None,filter_value:str=None):
    try:
        grade_data = (
            db.query(Grades)
            .join(Classes, Grades.class_id == Classes.class_id)
            .options(joinedload(Grades.classes).load_only(Classes.class_name))
            .filter(getattr(Grades,filter_column) == filter_value and Grades.is_deleted == False)
            .all()
        )
        return grade_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# create grade
@router.post("/create_grade/")
async def create_grade(grade:GradeBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        new_grade = Grades(**grade.dict())
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        grade = get_grade_by_filter(db,"grade_id",new_grade.grade_id)[0]
        return succes_response(jsonable_encoder(grade),msg="Grade Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get_grades_institute_wise
@router.get("/get_grades_institute/")
async def get_grades_institute_wise(institute_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grades = get_grade_by_filter(db,"institute_id",institute_id)
    return jsonable_encoder(grades)

# get_grade_by_field
@router.get("/get_grade_by_field/{field_name}/{field_value}/")
async def get_grade_by_field(field_name:str,field_value:str,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade = get_grade_by_filter(db,field_name,field_value)
    return jsonable_encoder(grade)

# get_grade_by_id
@router.get("/get_grade_by_id/")
async def get_grade_by_id(grade_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade = db.query(Grades).filter(Grades.grade_id == grade_id).first()
    if grade is None:
        raise HTTPException(status_code=500, detail=f"No ID Found")
    return jsonable_encoder(grade)

# update_grade  
@router.put("/update_grade/")
async def update_grade(grade_id:int,grade:GradeBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade_instance = db.query(Grades).filter(Grades.grade_id == grade_id).first()
    if grade_instance is None:
        raise HTTPException(status_code=500, detail=f"No ID Found")
    try:
        for key, value in grade.dict(exclude_unset=True).items():
            setattr(grade_instance, key, value)
        db.commit()
        db.refresh(grade_instance)
        return succes_response(grade_instance,msg="Grade Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Updating: {str(e)}")
    
# delete_grade
@router.delete("/delete_grade/")
async def delete_grade(grade_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade = db.query(Grades).filter(Grades.grade_id == grade_id).first()
    if grade is None:
        raise HTTPException(status_code=404,detail="Grade not Found.")
    db.delete(grade)
    db.commit()
    return succes_response(jsonable_encoder(grade),msg="Grade Deleted Successfully")

