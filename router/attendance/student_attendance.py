from datetime import date
from enum import Enum
import sys

from pydantic import validator
sys.path.append("..")
from router.basic_import import *
from models.attendance import StudentAttendance
from models.students import Student
from router.utility import succes_response
from sqlalchemy.orm import joinedload,Load,load_only

router = APIRouter()

class AttendaceStatus(str,Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"
    Holiday = "Holiday"


# base models
class StudentAttendanceBase(BaseModel):
    student_roll_number:str
    attendance_date: date =Field(default_factory=date.today)
    attendance_status: AttendaceStatus
    institute_id: int
    is_deleted: bool = False

    @validator('attendance_date')
    def attendance_date_must_be_valid(cls, v):
        if v > date.today():
            raise ValueError('Attendance date must be valid')
        return v

# create student attendance
@router.post("/create_student_attendance/")
async def create_student_attendance(attendance:StudentAttendanceBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    # checking student roll number is valid or not
    student = db.query(Student).filter(Student.roll_number == attendance.student_roll_number).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    # deleteing student_roll_number from attendance
    del attendance.student_roll_number
    try:
        new_attendance = StudentAttendance(**attendance.dict())
        new_attendance.student_id = student.student_id
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return succes_response(jsonable_encoder(new_attendance))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# get all student attendance
@router.get("/get_all_student_attendance/")
async def get_all_student_attendance(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        attendance = db.query(StudentAttendance).order_by(StudentAttendance.attendance_date.desc()).all()
        return jsonable_encoder(attendance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")


# get students attendance by institute id
@router.get("/get_student_attendance_by_institute_id/")
async def get_student_attendance_by_institute_id(institute_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        attendance = db.query(StudentAttendance).filter(StudentAttendance.institute_id == institute_id).order_by(StudentAttendance.attendance_date.desc()).all()
        return jsonable_encoder(attendance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")


# get student attendance by student id
@router.get("/get_student_attendance_by_student_id/")
async def get_student_attendance_by_student_id(student_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        attendance = (
            db.query(StudentAttendance)
            .join(Student,StudentAttendance.student_id == Student.student_id)
            .options(joinedload(StudentAttendance.student).load_only(Student.student_name))
            .filter(StudentAttendance.student_id == student_id)
            .order_by(StudentAttendance.attendance_date.desc())
            .all()
        )
        return jsonable_encoder(attendance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")


