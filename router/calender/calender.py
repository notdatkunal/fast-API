from datetime import date,datetime,time
from enum import Enum
import sys
sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.calender import Calender
from models import Classes,Sections,Subjects,Staff
from router.utility import succes_response


router = APIRouter()
class Days(str,Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"

class CalenderBase(BaseModel):
    institute_id: int
    class_id: int
    section_id: int
    subject_id: int
    staff_id: int
    day:Days
    start_time:time = Field(...,example="10:00:00")
    end_time:time = Field(...,example="11:00:00")

    @validator('start_time')
    def start_time_must_be_greater_than_end_time(cls, v, values, **kwargs):
        if 'end_time' in values and v > values['end_time']:
            raise ValueError('start_time must be greater than end_time')
        return v

# basic calender
def get_calender_by_filter(db=None,filter_column:str=None,filter_value:str=None):
    try:
        calender_data = (
            db.query(Calender)
            .join(Classes, Calender.class_id == Classes.class_id)
            .join(Sections, Calender.section_id == Sections.section_id)
            .join(Subjects, Calender.subject_id == Subjects.subject_id)
            .join(Staff, Calender.staff_id == Staff.staff_id)
            .options(joinedload(Calender.classes).load_only(Classes.class_name))
            .options(joinedload(Calender.sections).load_only(Sections.section_name))
            .options(joinedload(Calender.subjects).load_only(Subjects.subject_name))
            .options(joinedload(Calender.staffs).load_only(Staff.staff_name))
            .filter(getattr(Calender,filter_column) == filter_value and Calender.is_deleted == False)
            .all()
        )
        return calender_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/add_calender/")
async def add_calender(calender:CalenderBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        calender_instance = Calender(**calender.dict())
        db.add(calender_instance)
        db.commit()
        db.refresh(calender_instance)
        calender_instance = get_calender_by_filter(db,"calender_id",calender_instance.calender_id)
        return succes_response(calender_instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_calender_by_institute/")
async def get_all_calender(institute_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    calender = get_calender_by_filter(db,"institute_id",institute_id)
    return jsonable_encoder(calender)


@router.get("/get_calender_by_class&section/")
async def get_calender_by_class_and_section(class_id:int,section_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        calender = (
            db.query(Calender)
            .join(Classes, Calender.class_id == Classes.class_id)
            .join(Sections, Calender.section_id == Sections.section_id)
            .join(Subjects, Calender.subject_id == Subjects.subject_id)
            .join(Staff, Calender.staff_id == Staff.staff_id)
            .options(joinedload(Calender.classes).load_only(Classes.class_name))
            .options(joinedload(Calender.sections).load_only(Sections.section_name))
            .options(joinedload(Calender.subjects).load_only(Subjects.subject_name))
            .options(joinedload(Calender.staffs).load_only(Staff.staff_name))
            .filter(Calender.class_id == class_id and Calender.section_id == section_id and Calender.is_deleted == False)
            .order_by(Calender.day).all()
        )
        if calender is not None:
            return succes_response(calender)
        else:
            raise HTTPException(status_code=404, detail="Class not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_calender_by_staff/")
async def get_calender_by_staff(staff_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        calender = get_calender_by_filter(db,"staff_id",staff_id)
        if calender is not None:
            return succes_response(calender)
        else:
            raise HTTPException(status_code=404, detail="Class not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_calender_by_id/")
async def get_calender_data_by_id(calender_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        calender_data = get_calender_by_filter(db,"calender_id",calender_id)
        if calender_data is not None:
            return succes_response(calender_data)
        else:
            raise HTTPException(status_code=404, detail="Class not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))  


@router.put("/update_calender/")
async def update_calender(calender_id:int,calender:CalenderBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    calender_instance = db.query(Calender).filter(Calender.calender_id == calender_id).first()
    if calender_instance is None:
        raise HTTPException(status_code=404, detail="calender not found")
    try:
        for key ,value in calender.dict(exclude_unset=True).items():
            setattr(calender_instance, key ,value)
        db.commit()
        db.refresh(calender_instance)    
        return succes_response(calender_instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/delete_calender/")
async def delete_calender(calender_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        calender_data = db.query(Calender).filter(Calender.calender_id == calender_id).first()
        if calender_data is not None:
            calender_id = calender_data.calender_id
            db.delete(calender_data)
            db.commit()
            return succes_response({"calender_id":calender_id})
        else:
            raise HTTPException(status_code=404, detail="Class not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
