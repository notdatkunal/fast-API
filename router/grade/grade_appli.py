from datetime import date,datetime,time
from enum import Enum
import sys
sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.grade import Grades,GradeApplicable
from models.institute import Institute
from models.classes import Classes
from router.utility import succes_response

router = APIRouter()
# gradebase model
class GradeBase(BaseModel):
    institute_id:int
    grade_id :int
    class_id :int
    is_deleted :bool = False

def check_instance(model, field_name, field_value, db):
    try:
        model_instance = db.query(model).filter(getattr(model,field_name) == field_value and model.is_deleted == False).first()
        if model_instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def check_all_instances(value_institute, value_grade, value_class, db):
    check_instance(model=Institute, field_name="id", field_value=value_institute, db=db)
    check_instance(model=Grades, field_name="grade_id", field_value=value_grade, db=db)
    check_instance(model=Classes, field_name="class_id", field_value=value_class, db=db)

@router.post("/add_grade_applicable/")
async def add_grade_applicable(grade: GradeBase, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    try:
        check_all_instances(value_institute=grade.institute_id, value_grade=grade.grade_id, value_class=grade.class_id, db=db)
        grade_instance = GradeApplicable(**grade.dict())
        db.add(grade_instance)
        db.commit()
        db.refresh(grade_instance)
        return succes_response(grade_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/get_all_grade_applicable/")
async def get_all_grade_applicable(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grades = db.query(GradeApplicable).filter(GradeApplicable.is_deleted == False).order_by(GradeApplicable.id.desc()).all()
        return jsonable_encoder(grades)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/get_grade_applicable_by_class/")
async def get_grade_applicable_by_class(class_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    check_instance(model=Classes,field_name="class_id",field_value=class_id,db=db)
    try:
        grades = db.query(GradeApplicable).filter(GradeApplicable.class_id == class_id and GradeApplicable.is_deleted == False).order_by(GradeApplicable.id.desc()).all()
        return jsonable_encoder(grades)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get_grade_applicable_by_id/")
async def get_grade_applicable_by_id(id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade = db.query(GradeApplicable).filter(GradeApplicable.id == id and GradeApplicable.is_deleted == False).first()
        if grade is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        return succes_response(grade)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update_grade_applicable/")
async def update_grade_applicable(id:int,grade:GradeBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        check_all_instances(value_institute=grade.institute_id,value_grade=grade.grade_id,value_class=grade.class_id,db=db)
        grade_instance = db.query(GradeApplicable).filter(GradeApplicable.id == id and GradeApplicable.is_deleted == False).first()
        if grade_instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        for var, value in vars(grade).items():
            setattr(grade_instance, var, value) if value else None
        db.commit()
        db.refresh(grade_instance)
        return succes_response(grade_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete_grade_applicable/")
async def delete_grade_applicable(id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        grade_instance = db.query(GradeApplicable).filter(GradeApplicable.id == id and GradeApplicable.is_deleted == False).first()
        if grade_instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
        grade_instance.is_deleted = True
        db.commit()
        return succes_response("Grade deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
