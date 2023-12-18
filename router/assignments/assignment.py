from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.assignments import Assignments
from router.utility import succes_response
from sqlalchemy import Column,ForeignKey,Integer
router = APIRouter()
# base models
class AssignmentsBase(BaseModel):
    class_id: int
    section_id: int
    institute_id: int
    assignment_Date: date =Field(default_factory=date.today)
    assignment_title: str
    assignment_details: str
    assignment_due_date: date =Field(default_factory=date.today)
    is_deleted: bool = False

    institute_id = Column(Integer,ForeignKey("institute.id",ondelete="CASCADE"),nullable=True)    
    class_id = Column(Integer,ForeignKey("Tbl_Classes.class_id",ondelete="CASCADE"),nullable=True)
    section_id = Column(Integer,ForeignKey("Tbl_Sections.section_id",ondelete="CASCADE"),nullable=True)

# create assignment
@router.post("/create_assignment/")
async def create_assignment(assignment:AssignmentsBase,db:Session = Depends(get_db)):
    try:
        new_assignment = Assignments(**assignment.dict())
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        return succes_response(jsonable_encoder(new_assignment))
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get_assignments_institute_wise
@router.get("/get_assignments_institute/")
async def get_assignments_institute_wise(institution_id:int,db:Session = Depends(get_db)):
    assignments = ModelManager.get_data_by_institute(db.query(Assignments),Assignments,institution_id)
    return jsonable_encoder(assignments)

# get_assignment_by_field
@router.get("/get_assignment_by_field/{field_name}/{field_value}/")
async def get_assignment_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    assignment = ModelManager.get_data_by_field(db.query(Assignments),field_name,field_value,Assignments)
    return jsonable_encoder(assignment)

# get_assignment_by_id
@router.get("/get_assignment_by_id/")
async def get_assignment_by_id(assignment_id:int,db:Session = Depends(get_db)):
    try:
        assignment = db.query(Assignments).filter(Assignments.id == assignment_id).first()
        return jsonable_encoder(assignment)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"No ID Found")

# update_assignment
@router.put("/update_assignment/")
async def update_assignment(assignment_id:int,assignment:AssignmentsBase,db:Session = Depends(get_db)):
    try:
        assignment_data = db.query(Assignments).filter(Assignments.id == assignment_id).first()
        if assignment_data is not None:
            for key ,value in assignment.dict(exclude_unset=True).items():
                setattr(assignment_data, key ,value)
            db.commit()
            db.refresh(assignment_data)    
            return succes_response(assignment_data)
        else:
            raise HTTPException(status_code=404, detail="Assignment not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# delete_assignment
@router.delete("/delete_assignment/")
async def delete_assignment(assignment_id:int,db:Session = Depends(get_db)):
    try:
        assignment_data = db.query(Assignments).filter(Assignments.id == assignment_id).first()
        assignment_data.is_deleted = True
        db.commit()
        db.refresh(assignment_data)
        return succes_response(assignment_data)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Assignment not found")
