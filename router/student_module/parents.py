from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.students import Parents
from router.utility import succes_response
from sqlalchemy import Column,ForeignKey,Integer

router = APIRouter()
# base Model
class ParentBase(BaseModel):
    parent_name : str = Field(max_length=30)
    parent_email : str = Field(max_length=30)
    parent_phone : str = Field(min_length=10)
    parent_profile : Optional[str]
    parent_gender : Optional[str]
    parent_age : Optional[str]
    relation_with_student : str = Field(max_length=30)
    parent_address : Optional[str]
    parent_profession : Optional[str]
    photo : Optional[str]
    student_id:int

    # Foreign Keys
    student_id = Column(Integer,ForeignKey("students.student_id",ondelete="CASCADE"),nullable=True)


@router.post("/add_parent/")
async def create_parent(parent:ParentBase, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        new_parent = Parents(**parent.dict())
        db.add(new_parent)
        db.commit()
        db.refresh(new_parent)
        return {"status":"200","msg":"done",'response':new_parent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/all_Parents/")
async def get_all_parents(db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    parents = db.query(Parents).all()
    return jsonable_encoder(parents)


@router.get("/get_parent_data/")
async def get_parent_data_by_id(parent_id:int,db : Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    parent = db.query(Parents).filter(Parents.parent_id==parent_id).first()
    if parent is not None:
        return succes_response(jsonable_encoder(parent))
    else:
        raise HTTPException(status_code=404,detail="Parent data not Found.")
    
@router.put("/update_parent/")
async def update_parent_data(parent_id:int,parent_data: ParentBase,db : Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    parent_instance= db.query(Parents).filter(Parents.parent_id == parent_id).first()
    if parent_data is not None:
        for key, value in parent_data.dict(exclude_unset=True).items(): 
            setattr(parent_instance, key, value)
        db.commit()
        db.refresh(parent_instance)
        return succes_response(parent_instance)
    else:
        raise HTTPException(status_code=404, detail="Parent not found")

# for student form below code 
@router.get("/parent/student_id")
async def get_parent_data_by_id(student_id:int, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    parent_data = db.query(Parents).filter(Parents.student_id == student_id).all()
    if parent_data is not None:
        return succes_response(jsonable_encoder(parent_data))
    else:
        raise HTTPException(status_code=404, detail="Parent not found")

@router.put("/update/{student_id}")
async def update_student(student_id: int, student: ParentBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    parent_data = db.query(Parents).filter(Parents.student_id == student_id).first()
    if parent_data is not None:
        for key, value in student.dict(exclude_unset=True).items(): 
            setattr(parent_data, key, value)
        db.commit()
        db.refresh(parent_data)
        return succes_response(parent_data)
    else:
        raise HTTPException(status_code=404, detail="Parent not found")
