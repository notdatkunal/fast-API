from database import BASE
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float
import sys

sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.classes import Classes
from models.examination import ParentExam, Exam, ResultEntry
from models.grade import Grades, grades_classes_association
from models.students import Student
from router.utility import succes_response
ResultEntry.__table__.create(bind=engine, checkfirst=True)

router = APIRouter()
class ResultEntryBase(BaseModel):
    exam_id: int
    student_id: int
    result: dict
    is_deleted: bool = False

def generate_result(exam_subjects, result):
    result_data = {}
    marks = []
    total_marks = 0
    total_obtained_marks = 0
    for exam_subject in exam_subjects:
        subject_name = exam_subject.subject.subject_name
        subject_marks = result.get(subject_name, 0)
        row = {
            "subject_name": subject_name,
            "full_marks": exam_subject.full_marks,
            "obtained_marks": subject_marks,
            "grade": "A"
        }
        marks.append(row)
        total_marks += exam_subject.full_marks
        total_obtained_marks += subject_marks

    result_data["marks"] = marks
    result_data["total_marks"] = total_marks
    result_data["total_obtained_marks"] = total_obtained_marks
    result_data["percentage"] = round((total_obtained_marks / total_marks) * 100, 2)
    result_data["grade"] = "A"
    return result_data

@router.post("/result_entry")
async def result_entry(result_entry: ResultEntryBase, db: Session = Depends(get_db)):
    parent_exam = db.query(ParentExam).filter(ParentExam.parent_exam_id == result_entry.exam_id).first()
    if parent_exam is None:
        return HTTPException(status_code=404, detail="Parent Exam Not Found")
    student = db.query(Student).filter(Student.student_id == result_entry.student_id).first()
    if student is None:
        return HTTPException(status_code=404, detail="Student Not Found")
    exam_subjects =  db.query(Exam).filter(Exam.parent_exam_id == result_entry.exam_id).all()
    if exam_subjects is None:
        return HTTPException(status_code=404, detail="Exam Subject Not Found")
    is_student_exist =  db.query(ResultEntry).filter(ResultEntry.student_id == result_entry.student_id).first()
    if is_student_exist is not None:
        return HTTPException(status_code=404, detail="Result Already Exist")
    try:
        result_data = generate_result(exam_subjects, result_entry.result)
        result_entry.result = result_data
        result_entry = ResultEntry(**result_entry.dict())
        db.add(result_entry)
        db.commit()
        db.refresh(result_entry)
        return succes_response(result_entry)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
def get_result_data(db,filder_by,filder_value):
    result_data =(
        db.query(ResultEntry)
        .join(ParentExam,ParentExam.parent_exam_id == ResultEntry.exam_id)
        .join(Student,Student.student_id == ResultEntry.student_id)
        .options(joinedload(ResultEntry.parent_exam).load_only(ParentExam.parent_exam_name))
        .options(joinedload(ResultEntry.student).load_only(Student.student_name,Student.roll_number))
        .filter(getattr(ResultEntry,filder_by) == filder_value)
        .all()
    )
    return result_data
    
# get result all result entry
@router.get("/get_all_result_entry/")
async def get_all_result_entry(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        result_entry = db.query(ResultEntry).all()
        return jsonable_encoder(result_entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")
    

# get result entry by parent_exam_id
@router.get("/get_result_entry_by_parent_exam_id/")
async def get_result_entry_by_parent_exam_id(parent_exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    parent_exam = db.query(ParentExam).filter(ParentExam.parent_exam_id == parent_exam_id).first()
    if parent_exam is None:
        raise HTTPException(status_code=404, detail="Parent Exam Not Found")
    result_entry = get_result_data(db,"exam_id",parent_exam_id)
    return jsonable_encoder(result_entry)
