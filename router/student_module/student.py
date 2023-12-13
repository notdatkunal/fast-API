from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.students import Student
from router.utility import succes_response

router = APIRouter()

# student base model
class StudentBase(BaseModel):
    institute_id :int
    student_name :str = Field(min_length=3,max_length=30)
    gender :str = Field(min_length=2)
    date_of_birth :date = Field(default_factory=date.today)
    blood_group :str
    address :Optional[str]
    phone_number :str = Field(min_length=10)
    email :Optional[str]
    admission_date :date
    roll_number :str =Field(max_length=20)
    photo :str
    slug :str
    # foreign keys
    class_id :int
    section_id :int
    transport_id :Optional[int]

@router.get("/get_all_students/")
async def get_all_students(db:Session = Depends(get_db)):
    students = db.query(Student).all()
    return jsonable_encoder(students)

@router.post("/create_student/")
async def create_student(student:StudentBase,db:Session = Depends(get_db)):
    try:
        new_student = Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"statu":"200","msg":"done",'response':new_student}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
@router.put("/update_student/{student_id}")
async def update_student(student_id: int, student: StudentBase, db: Session = Depends(get_db)):
    # Use .first() to execute the query and retrieve the first result
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        for key, value in student.dict(exclude_unset=True).items():
            setattr(student_data, key, value)
        db.commit()
        db.refresh(student_data)
        return {"status":"200","msg":"done",'response':student_data}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.get("/get_student/")
async def get_student_data_by_id(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        return {"status":"200","msg":"done",'response':student_data}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/delete_student/")
async def delete_student(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        student_id = student_data.student_id
        db.delete(student_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"student_id":student_id}}
    else:
        raise HTTPException(status_code=404, detail="Student not found")