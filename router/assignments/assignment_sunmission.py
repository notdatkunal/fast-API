from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.assignments import Assignments,AssignmentSubmission
from models.students import Student
from router.utility import succes_response
from sqlalchemy import Column,ForeignKey,Integer
from sqlalchemy.orm import joinedload,Load,load_only

router = APIRouter()

# base models
class AssignmentSubmissionBase(BaseModel):
    assignment_id: int
    student_id: int
    submission_date: date = Field(default_factory=date.today)
    submission_details: str
    assignment_file: str
    is_deleted: bool = False


# basic assignment
def get_assgiment_submission(db=None,filter_column=None,filter_value=None):
    try:
        Assignments_submission_data =(
            db.query(AssignmentSubmission)
            .join(Assignments,AssignmentSubmission.assignment_id == Assignments.id)
            .join(Student,AssignmentSubmission.student_id == Student.student_id)
            .options(
                joinedload(AssignmentSubmission.assignments).load_only(Assignments.assignment_title),
                joinedload(AssignmentSubmission.students).load_only(Student.student_name)
            )
            .filter(getattr(AssignmentSubmission,filter_column) == filter_value and AssignmentSubmission.is_deleted == False)
            .order_by(AssignmentSubmission.id.desc())
            .all()
        )
        return jsonable_encoder(Assignments_submission_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# create submission
@router.post("/submit_assignment/")
async def submit_assignment(assignment_submission:AssignmentSubmissionBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if db.query(Assignments).filter(Assignments.id == assignment_submission.assignment_id).first() is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if db.query(Student).filter(Student.student_id == assignment_submission.student_id).first() is None:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        assignment_submission_instance = AssignmentSubmission(**assignment_submission.dict())
        db.add(assignment_submission_instance)
        db.commit()
        db.refresh(assignment_submission_instance)
        assignment_submission_instance = get_assgiment_submission(db,"id",assignment_submission_instance.id)
        return succes_response(assignment_submission_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# get assignment submission by assignment id
@router.get("/get_assignment_submission_by_assignment_id/")
async def get_assignment_submission_by_assignment_id(assignment_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    assignment_submission = get_assgiment_submission(db,"assignment_id",assignment_id)
    return succes_response(assignment_submission)

# get assignment submission by student id
@router.get("/get_assignment_submission_by_student_id/")
async def get_assignment_submission_by_student_id(student_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    assignment_submission = get_assgiment_submission(db,"student_id",student_id)
    return succes_response(assignment_submission)

# get assignment submission by assignment submission id
@router.get("/get_assignment_submission_by_id/")
async def get_assignment_submission_by_id(id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    assignment_submission = get_assgiment_submission(db,"id",id)
    return succes_response(assignment_submission)

# update assignment submission
@router.put("/update_assignment_submission/")
async def update_assignment_submission(assignment_submission_id:int,assignment_submission:AssignmentSubmissionBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if db.query(Assignments).filter(Assignments.id == assignment_submission.assignment_id).first() is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if db.query(Student).filter(Student.student_id == assignment_submission.student_id).first() is None:
        raise HTTPException(status_code=404, detail="Student not found")

    assignment_submission_instance = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == assignment_submission_id).first()
    if assignment_submission_instance is None:
        raise HTTPException(status_code=404, detail="Assignment submission not found")
    try:
        assignment_submission_instance.assignment_id = assignment_submission.assignment_id
        assignment_submission_instance.student_id = assignment_submission.student_id
        assignment_submission_instance.submission_date = assignment_submission.submission_date
        assignment_submission_instance.submission_details = assignment_submission.submission_details
        assignment_submission_instance.assignment_file = assignment_submission.assignment_file
        db.commit()
        assignment_submission_instance = get_assgiment_submission(db,"id",assignment_submission_instance.id)
        return succes_response(assignment_submission_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# delete assignment submission
async def delete_assignment_submission(assignment_submission_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    assignment_submission_instance = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == assignment_submission_id).first()
    if assignment_submission_instance is None:
        raise HTTPException(status_code=404, detail="Assignment submission not found")
    try:
        assignment_submission_instance.is_deleted = True
        db.commit()
        assignment_submission_instance = get_assgiment_submission(db,"id",assignment_submission_instance.id)
        return succes_response(assignment_submission_instance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
