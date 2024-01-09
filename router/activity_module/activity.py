from datetime import date
from enum import Enum
import sys
sys.path.append("..")
from router.basic_import import *
from models.activity import Activity
from models.students import Student
from models.institute import Institute
from router.utility import succes_response
Activity.metadata.create_all(bind=engine)

router = APIRouter()

# base models   
class ActivityBase(BaseModel):
    institution_id: int
    activity_name: str = Field(min_length=3)
    activity_description:Optional[str] = None
    activity_date: date = Field(default_factory=date.today)
    activity_location:Optional[str] = None
    is_deleted: bool = False
    student_id: Optional[int] = Field(default=None)

# post method code
@router.post("/create_activity/")
async def post_activity_data(activity:ActivityBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    student = None
    if activity.student_id != 0:
        student = db.query(Student).filter(Student.student_id == activity.student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        elif student.institute_id != activity.institution_id:
            raise HTTPException(status_code=404, detail="Student not belongs to this institute")
    else:
        activity.student_id = None
    try:
        activity_instance = Activity(**activity.dict())
        db.add(activity_instance)
        db.commit()
        db.refresh(activity_instance)
        return succes_response(activity_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# get all activity by institute id
@router.get("/get_all_activity_by_institute/")
async def get_all_activity_by_institute(institution_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    activity_data = (
        db.query(Activity)
        .filter(Activity.institution_id == institution_id,Activity.is_deleted == False)
        .options(joinedload(Activity.students).load_only(Student.student_name))
        .order_by(Activity.activity_id.desc())
        .all()
    )
    return jsonable_encoder(activity_data)

# get all activity by student id
@router.get("/get_all_activity_by_student/")
async def get_all_activity_by_student(student_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    activity_data = (
        db.query(Activity)
        .join(Student,Activity.student_id == Student.student_id)
        .filter(Activity.student_id == student_id,Activity.is_deleted == False)
        .options(joinedload(Activity.students).load_only(Student.student_name))
        .order_by(Activity.activity_id.desc())
        .all()
    )
    return jsonable_encoder(activity_data)

# get all activity by id
@router.get("/get_activity_by_id/")
async def get_activity_by_id(activity_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    activity_data = (
        db.query(Activity)
        .filter(Activity.activity_id == activity_id,Activity.is_deleted == False)
        .options(joinedload(Activity.students).load_only(Student.student_name))
        .first()
    )
    if activity_data is not None:
        return succes_response(activity_data)
    else:
        raise HTTPException(status_code=404, detail="Activity not found")


@router.put('update_activity/')
async def update_activity(actity_id:int,activity:ActivityBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    activity_data = db.query(Activity).filter(Activity.activity_id == actity_id).first()
    if activity_data is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.student_id != 0:
        student = db.query(Student).filter(Student.student_id == activity.student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        elif student.institute_id != activity.institution_id:
            raise HTTPException(status_code=404, detail="Student not belongs to this institute")
    else:
        activity.student_id = None
    if db.query(Institute).filter(Institute.id == activity.institution_id).first() is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    try:
        for key, value in activity.dict(exclude_unset=True).items(): 
            setattr(activity_data, key, value)
        db.commit()
        db.refresh(activity_data)
        return succes_response(activity_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/delete_activity/")
async def delete_activity(activity_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    activity_data = db.query(Activity).filter(Activity.activity_id == activity_id).first()
    if activity_data is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity_data)
    db.commit()
    return succes_response("Activity Deleted Successfully")
