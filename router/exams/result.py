from time import perf_counter
from database import BASE
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float, func
import sys
import asyncio

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

class ResultEntryFrontEnd(BaseModel):
    student_roll_number:str
    result: dict
    is_deleted: bool = False


class BulkResultEntry(BaseModel):
    exam_id: int
    data:list

def get_grade(db=None, percentage=None, class_id=None):
    grade = db.query(Grades)\
        .join(grades_classes_association)\
        .filter(
            Grades.percent_from <= percentage,
            Grades.percent_upto >= percentage,
            grades_classes_association.c.class_id == class_id
        ).first()
    if grade is None:
        return None
    return grade.grade_name

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
        result_data = generate_result(exam_subjects=exam_subjects, result=result_entry.result, class_id=parent_exam.class_id,db=db)
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
    

# counting result according to grade

def counting_grades(db: db_dependency, parent_exam_id):
    try:
        count = (
            db.query(ResultEntry.result["grade"].label("grade"), func.count().label("grade_count"))
            .filter(ResultEntry.exam_id == parent_exam_id)
            .group_by(ResultEntry.result["grade"])
            .all()
        )
        return [{"grade": row.grade, "grade_count": row.grade_count} for row in count]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")

async def calculate_ranking(parent_exam_id: int, db: db_dependency):
    try:
        result = (
            db.query(
                ResultEntry.student_id,
                ResultEntry.result["percentage"].label("percentage"),
                func.dense_rank().over(order_by=ResultEntry.result["percentage"].desc()).label("rank")
            )
            .filter(ResultEntry.exam_id == parent_exam_id)
            .order_by(ResultEntry.result["percentage"].desc())
        )
        result = result.all()
        # Formatting the result
        formatted_result = [
            {
                "student_id": row[0],
                "percentage": row[2],
                "rank": row[1],
                "student":db.query(Student).filter(Student.student_id == row[0]).first(),
            }
            for row in result
        ]

        return {"success": True, "data": formatted_result, "msg": "Ranking calculated successfully"}
    except Exception as e:
        return {"success": False, "error": f"Error While Calculating Ranking: {str(e)}"}

# get result entry by parent_exam_id
@router.get("/get_result_entry_by_parent_exam_id/")
async def get_result_entry_by_parent_exam_id(parent_exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    parent_exam = db.query(ParentExam).filter(ParentExam.parent_exam_id == parent_exam_id).first()
    count = counting_grades(db,parent_exam_id)
    if parent_exam is None:
        raise HTTPException(status_code=404, detail="Parent Exam Not Found")
    result_entry = get_result_data(db,"exam_id",parent_exam_id)
    rank = await asyncio.create_task(calculate_ranking(parent_exam_id, db))
    print(rank)
    payload = {
        "result_entry": result_entry,
        "count": jsonable_encoder(count)
    }
    return succes_response(payload)

# create bulk result entry
@router.post("/bulk_result_entry")
async def bulk_result_entry(bulk_result_entry: BulkResultEntry, db: db_dependency):
    start = perf_counter()
    exam_id = bulk_result_entry.exam_id
    result_data = bulk_result_entry.data
    parent_exam = (
        db.query(ParentExam)
        .filter(ParentExam.parent_exam_id == exam_id)
        .first()
    )
    if parent_exam is None:
        raise HTTPException(status_code=404, detail="Parent Exam Not Found")
    exam_subjects = (
        db.query(Exam).filter(Exam.parent_exam_id == parent_exam.parent_exam_id).all()
    )
    if not exam_subjects:
        raise HTTPException(status_code=404, detail="Exam Subjects Not Found")
    exam_subjects = [{"subject_name": exam_subject.subject.subject_name, "full_marks": exam_subject.full_marks} for exam_subject in exam_subjects]
    try:
        for result_entry in result_data:
            student = (
                db.query(Student)
                .filter(
                    Student.roll_number == result_entry[1],
                    Student.class_id == parent_exam.class_id,
                )
                .first()
            )
            if student is None:
                continue
            result_data = await asyncio.create_task(
                generate_result(exam_subjects=exam_subjects, result=result_entry[2:], class_id=parent_exam.class_id,db=db)
                )
            result = ResultEntry(
                exam_id=parent_exam.parent_exam_id,
                student_id=student.student_id,
                result=result_data,
            )
            existing_result = (
                db.query(ResultEntry)
                .filter(ResultEntry.student_id == student.student_id)
                .first()
            )
            if existing_result:
                existing_result.result = result_data
            else:
                db.add(result)
        db.commit()
        end = perf_counter()
        print("Time Taken: ", end - start)
        return succes_response(data="", msg="Result Entry Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get result entry by student_id and parent_exam_id
@router.get("/get_result_entry_by_student_id_and_parent_exam_id/")
async def get_result_entry_by_student_id_and_parent_exam_id(student_id:int,parent_exam_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    parent_exam = db.query(ParentExam).filter(ParentExam.parent_exam_id == parent_exam_id).first()
    if parent_exam is None:
        raise HTTPException(status_code=404, detail="Parent Exam Not Found")
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")
    try:
        result_entry =(
            db.query(ResultEntry)
            .join(ParentExam,ParentExam.parent_exam_id == ResultEntry.exam_id)
            .join(Student,Student.student_id == ResultEntry.student_id)
            .options(joinedload(ResultEntry.parent_exam).load_only(ParentExam.parent_exam_name))
            .options(joinedload(ResultEntry.student).load_only(Student.student_name,Student.roll_number))
            .filter(ResultEntry.student_id == student_id,ResultEntry.exam_id == parent_exam_id)
            .first()
        )
        return succes_response(data=result_entry,msg="Result Entry Found Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")
    


async def generate_result(exam_subjects=None, result=None, class_id=None, db=None):
    result_data = {"marks": []}
    total_marks = 0
    total_obtained_marks = 0
    for ind in range(len(exam_subjects)):
        exam_subject = exam_subjects[ind]
        subject_name = exam_subject["subject_name"]
        subject_marks = result[1]
        full_marks = exam_subject["full_marks"]

        row = {
            "subject_name": subject_name,
            "full_marks": full_marks,
            "obtained_marks": subject_marks,
            "percentage": round((subject_marks / full_marks) * 100, 2),
            "grade": None 
        }

        result_data["marks"].append(row)
        total_marks += full_marks
        total_obtained_marks += subject_marks

    overall_percentage = round((total_obtained_marks / total_marks) * 100, 2)

    for row in result_data["marks"]:
        row["grade"] =get_grade(db=db, percentage=row["percentage"], class_id=class_id)

    result_data["total_marks"] = total_marks
    result_data["total_obtained_marks"] = total_obtained_marks
    result_data["percentage"] = overall_percentage
    result_data["grade"] = get_grade(db=db, percentage=overall_percentage, class_id=class_id)

    return result_data

