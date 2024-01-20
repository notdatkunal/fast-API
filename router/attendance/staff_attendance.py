from datetime import date
from enum import Enum
import sys
from pydantic import validator
sys.path.append("..")
from router.basic_import import *
from models.attendance import StaffAttendance
from models.staffs import Staff
from router.utility import succes_response
from sqlalchemy.orm import joinedload,Load,load_only

router = APIRouter()

class AttendaceStatus(str,Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"

# base models
class StaffAttendanceBase(BaseModel):
    employee_id:str
    attendance_date: date =Field(default_factory=date.today)
    attendance_status: AttendaceStatus
    institute_id: int
    is_deleted: bool = False

    @validator('attendance_date')
    def attendance_date_must_be_valid(cls, v):
        if v > date.today():
            raise ValueError('Attendance Date must be Current date or Past Dates')
        return v
    

class StaffBulkAttendanceBase(BaseModel):
    staff_id:int
    attendance_date: date =Field(default_factory=date.today)
    attendance_status: AttendaceStatus
    institute_id: int
    is_deleted: bool = False

class BulkData(BaseModel):
    data: List[StaffBulkAttendanceBase]


# basic attendance
def get_staff_attendance_by_filter(db=None,filter_column:str=None,filter_value:str=None):
    try:
        attendance_data = (
            db.query(StaffAttendance)
            .join(Staff,StaffAttendance.staff_id == Staff.staff_id)
            .options(joinedload(StaffAttendance.staff).load_only(Staff.staff_name,Staff.employee_id))
            .filter(getattr(StaffAttendance,filter_column) == filter_value,StaffAttendance.is_deleted == False)
            .order_by(StaffAttendance.attendance_date.desc())
            .all()
        )
        return attendance_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_staff_attendance_by_institute(institute_id,db):
    absent_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.institute_id == institute_id, StaffAttendance.attendance_status == "Absent")
        .count()
    )
    present_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.institute_id == institute_id, StaffAttendance.attendance_status == "Present")
        .count()
    )
    
    total_attendance_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.institute_id == institute_id)
        .count()
    )
    if total_attendance_count > 0:
        absent_percentage = (absent_count / total_attendance_count) * 100
        present_percentage = (present_count / total_attendance_count) * 100
        leave_percentage = 100 - (absent_percentage + present_percentage)
        return {"absent_percentage": absent_percentage, "present_percentage": present_percentage, "leave_percentage": leave_percentage}
    return {"absent_percentage": 0, "present_percentage": 0, "leave_percentage": 0}

def get_staff_attendance(staff_id, db):
    absent_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.staff_id == staff_id, StaffAttendance.attendance_status == "Absent")
        .count()
    )
    present_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.staff_id == staff_id, StaffAttendance.attendance_status == "Present")
        .count()
    )
    total_attendance_count = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.staff_id == staff_id)
        .count()
    )
    if total_attendance_count > 0:
        absent_percentage = round((absent_count / total_attendance_count) * 100,2)
        present_percentage = round((present_count / total_attendance_count) * 100,2)
        return {"absent_percentage": absent_percentage, "present_percentage": present_percentage}
    return {"absent_percentage": 0, "present_percentage": 0}


# create staff attendance
@router.post("/create_staff_attendance/")
async def create_staff_attendance(attendance:StaffAttendanceBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    # checking staff id is valid or not
    staff = db.query(Staff).filter(Staff.employee_id == attendance.employee_id).first()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    # deleteing staff_id from attendance
    del attendance.employee_id
    # checking attendance is already taken or not
    if db.query(StaffAttendance).filter(StaffAttendance.attendance_date == attendance.attendance_date).first() is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Attendance already taken")
    try:
        new_attendance = StaffAttendance(**attendance.dict())
        new_attendance.staff_id = staff.staff_id
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        new_attendance = get_staff_attendance_by_filter(db,"id",new_attendance.id)
        return succes_response(jsonable_encoder(new_attendance),msg="Attendance Taken Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# get all staff attendance
@router.get("/get_all_staff_attendance/")
async def get_all_staff_attendance(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        attendance = db.query(StaffAttendance).order_by(StaffAttendance.attendance_date.desc()).all()
        return jsonable_encoder(attendance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Getting: {str(e)}")


# get staff attendance by institute id
@router.get("/get_staff_attendance_by_institute_id/")
async def get_staff_attendance_by_institute_id(institute_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    attendance_data = get_staff_attendance_by_filter(db,"institute_id",institute_id)
    payload = {
        "attendance_data":attendance_data,
        "attendance_percentage":get_staff_attendance_by_institute(institute_id,db)
    }
    return jsonable_encoder(payload)


# get staff attendance by staff id
@router.get("/get_staff_attendance_by_staff_id/")
async def get_staff_attendance_by_staff_id(staff_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    staff_attendance = get_staff_attendance_by_filter(db,"staff_id",staff_id)
    payload = {
        "staff_attendance":staff_attendance,
        "staff_attendance_percentage":get_staff_attendance(staff_id,db)
    }
    return jsonable_encoder(payload)


# creating bulk staff attendance according class
@router.post("/create_bulk_staff_attendance/")
async def create_bulk_staff_attendance(bulk_data: BulkData, db: db_dependency):
    staff_data = bulk_data.data
    payload = []
    try:
        for data in staff_data:
            is_having_attendance = db.query(StaffAttendance).filter(StaffAttendance.attendance_date == data.attendance_date, StaffAttendance.staff_id == data.staff_id).first()
            if is_having_attendance is not None:
                continue
            attendance = StaffAttendance(**data.dict())
            db.add(attendance)
            db.refresh(attendance)
            db.commit()  
            attendance = get_staff_attendance_by_filter(db,"id",attendance.id)
            payload.append(attendance)
        return succes_response(data=payload, msg="Attendance Taken Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get staff attendance by id
@router.get("/get_staff_attendance_by_id/")
async def get_staff_attendance_by_id(attendance_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        attendance = get_staff_attendance_by_filter(db,"id",attendance_id)
        if attendance is None:
            raise HTTPException(status_code=404, detail="Attendance Not Found")
        return jsonable_encoder(attendance)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Occured: {e}")    


# patch medthod
@router.patch("/update_staff_attendance/")
async def update_staff_attendance(attendance_id:int,db:db_dependency,current_user: str = Depends(is_authenticated),data: dict ={}):
    try:
        attendance = db.query(StaffAttendance).filter(StaffAttendance.id == attendance_id).first()
        if attendance is None:
            raise HTTPException(status_code=404, detail="Attendance Not Found")
        for key, value in data.items():
            setattr(attendance, key, value)
        db.commit()
        db.refresh(attendance)
        attendance = get_staff_attendance_by_filter(db,"id",attendance_id)
        return succes_response(attendance, msg="Attendance Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Occured: {e}")


