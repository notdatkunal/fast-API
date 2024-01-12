from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.grade import Grades,grades_classes_association
from models import Classes
from router.utility import succes_response
from sqlalchemy.orm import contains_eager

router = APIRouter()

# base models
class GradeBase(BaseModel):
    institute_id:int
    class_id:List[int]
    grade_name:str = Field(min_length=1)
    percent_from: int
    percent_upto: int
    is_deleted: bool = False

# basic grade
def get_grade_by_filter(db=None,filter_column:str=None,filter_value:str=None):
    try:
        grade_data =(
            db.query(Grades)
            .join(grades_classes_association,grades_classes_association.c.grade_id == Grades.grade_id)
            .join(Classes,Classes.class_id == grades_classes_association.c.class_id)
            .filter(getattr(Grades,filter_column) == filter_value)
            .options(contains_eager(Grades.grades))
            .all()
        )
        return grade_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

#  create asssiociation
async def create_association(db=None,grade_id:int=None,class_id:List[int]=None):
    try:
        for i in class_id:
            association = grades_classes_association.insert().values(grade_id=grade_id,class_id=i)
            db.execute(association)
            db.commit()
        return "Association Created Successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_association(db=None,grade_id:int=None,class_id:List[int]=None):
    try:
        # delete all existing association
        db.query(grades_classes_association).filter(grades_classes_association.c.grade_id == grade_id).delete(synchronize_session=False)
        db.commit()
        # create new association
        for i in class_id:
            association = grades_classes_association.insert().values(grade_id=grade_id,class_id=i)
            db.execute(association)
            db.commit()
        return "Association Updated Successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_association(db=None,grade_id:int=None):
    try:
        # delete all existing association
        db.query(grades_classes_association).filter(grades_classes_association.c.grade_id == grade_id).delete(synchronize_session=False)
        db.commit()
        return "Association Deleted Successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# create grade
@router.post("/create_grade/")
async def create_grade(grade:GradeBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        new_grade = Grades() # create new instance
        new_grade.institute_id = grade.institute_id
        new_grade.grade_name = grade.grade_name
        new_grade.percent_from = grade.percent_from
        new_grade.percent_upto = grade.percent_upto
        new_grade.is_deleted = grade.is_deleted
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        await create_association(db,new_grade.grade_id,grade.class_id)
        new_grade = get_grade_by_filter(db,"grade_id",new_grade.grade_id)
        return succes_response(jsonable_encoder(new_grade),msg="Grade Created Successfully")
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
    grade = get_grade_by_filter(db,"grade_id",grade_id)[0]
    if grade is None:
        raise HTTPException(status_code=500, detail=f"No ID Found")
    return jsonable_encoder(grade)

# get_grade_by_class_id
@router.get("/get_grade_by_class_id/")
async def get_grade_by_class_id(class_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade = (
        db.query(Grades)
        .join(grades_classes_association,grades_classes_association.c.grade_id == Grades.grade_id)
        .join(Classes,Classes.class_id == grades_classes_association.c.class_id)
        .filter(Classes.class_id == class_id)
        .options(contains_eager(Grades.grades))
        .all()
    )
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
        await update_association(db,grade_id,grade.class_id)
        grade = await get_grade_by_id(grade_id,db)
        return succes_response(grade,msg="Grade Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Updating: {str(e)}")
    
# delete_grade
@router.delete("/delete_grade/")
async def delete_grade(grade_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    grade = db.query(Grades).filter(Grades.grade_id == grade_id).first()
    if grade is None:
        raise HTTPException(status_code=404,detail="Grade not Found.")
    await delete_association(db,grade_id)
    db.delete(grade)
    db.commit()
    return succes_response(jsonable_encoder(grade),msg="Grade Deleted Successfully")

