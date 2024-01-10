from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.grade import Grades
from models.students import Student
from models.classes import Classes
from models.examination import ParentExam,Exam
from router.utility import succes_response
import asyncio

router = APIRouter()

class StudentInfo:
    def __init__(self, student_id):
        self.student_id = student_id
    
    async def get_student_data(self, db):
        db_student = db.query(Student).filter(Student.student_id == self.student_id).first()
        return db_student
    
    async def get_exams_data(self,class_id,db):
        try:
            upcoming_parent_exam = (
                db.query(ParentExam)
                .join(Classes,ParentExam.class_id == Classes.class_id)
                .options(joinedload(ParentExam.classes).load_only(Classes.class_name))
                .filter(ParentExam.class_id == class_id,ParentExam.start_date >= date.today())
                .order_by(ParentExam.start_date.desc())
                .all()
            )
            old_parent_exams = (
                db.query(ParentExam)
                .join(Classes,ParentExam.class_id == Classes.class_id)
                .options(joinedload(ParentExam.classes).load_only(Classes.class_name))
                .filter(ParentExam.class_id == class_id,ParentExam.start_date < date.today())
                .order_by(ParentExam.start_date.desc())
                .all()
            )
            return jsonable_encoder({"upcoming_parent_exam":upcoming_parent_exam,"old_parent_exams":old_parent_exams})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")

    async def  collect_all_data(self,db):
        student_data = await asyncio.gather(self.get_student_data(db))
        exam_data = await asyncio.gather(self.get_exams_data(student_data.class_id,db))
        payload = {
            "student_data": student_data,
            "exam_data": exam_data
        }
        return payload


@router.get("/get_all_student_data/")
async def get_all_student_data(student_id: int, db: db_dependency):
    try:
        students = StudentInfo(student_id)
        students_data = students.get_student_data(db)
        exam_data = students.get_exams_data(students_data.class_id,db)
        payload = {
            "student_data": students_data,
            "exam_data": exam_data
        }
        return jsonable_encoder(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

        