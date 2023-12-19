from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.students import Student
from models import Classes,Transport,Sections
from models.manager import ModelManager
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

# geting all student according to institute id
@router.get("/get_students_by_intitute/")
async def get_all_students( institute_id:int,db:Session = Depends(get_db)):
    students = ModelManager.get_student_data_by_institute(db.query(Student),institute_id)
    students_data = return_student_data_with_names(students,db)
    return jsonable_encoder(students_data)

@router.get("/get_students_by_field/{field_name}/{field_value}/")
async def get_all_students_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    student_model = Student
    students = ModelManager.get_data_by_field(db.query(student_model),field_name,field_value,student_model)
    return jsonable_encoder(students)


def return_student_data_with_names(student_data,db):
    for student in student_data:
        student.class_id =db.get(Classes,student.class_id).class_name
        student.section_id = db.query(Sections).get(student.section_id).section_name
        student.transport_id = db.query(Transport).get(student.transport_id).transport_name
    return student_data

# creating student data
@router.post("/create_student/")
async def create_student(student: StudentBase, db: Session = Depends(get_db)):
    try:
        # Create a new Student instance with the provided data
        new_student = Student(**student.dict())

        # Add, commit, and refresh the new student
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        # Fetch the new student data, including foreign keys' names
        new_student_with_names = db.query(Student).filter(Student.student_id == new_student.student_id).first()
        # Convert foreign keys' names to IDs
        new_student_with_names.class_id = db.query(Classes).get(new_student_with_names.class_id).class_name
        new_student_with_names.section_id = db.query(Sections).get(new_student_with_names.section_id).section_name
        new_student_with_names.transport_id = db.query(Transport).get(new_student_with_names.transport_id).transport_name
        return succes_response(new_student_with_names)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")



# updating student data
@router.put("/update_student/{student_id}")
async def update_student(student_id: int, student: StudentBase, db: Session = Depends(get_db)):
    # Use .first() to execute the query and retrieve the first result
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        for key, value in student.dict(exclude_unset=True).items():
            setattr(student_data, key, value)
        db.commit()
        db.refresh(student_data)
        return succes_response(student_data)
    else:
        raise HTTPException(status_code=404, detail="Student not found")


# geting student data by id
@router.get("/get_student/")
async def get_student_data_by_id(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        return succes_response(student_data)
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# deleteing the students
@router.delete("/delete_student/")
async def delete_student(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        student_id = student_data.student_id
        db.delete(student_data)
        db.commit()
        return {"status": "200", "msg": "done", 'response':student_id}
    else:
        raise HTTPException(status_code=404, detail="Student not found")