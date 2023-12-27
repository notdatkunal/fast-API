from datetime import date
import sys
import uuid
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
    photo :str
    # foreign keys
    class_id :int
    section_id :int

# genarating slug using student name and student class
def generate_slug(student_name:str,db):
    slug = student_name.replace(" ","-")
    while True:
        if db.query(Student).filter(Student.slug == slug).first():
            slug = slug + str(uuid.uuid4())[:6]
        else:
            return slug
        
# genarate rollnumber using student class and section and institute id
def generate_roll_number(class_id: int, section_id: int, institute_id: int, db):
    class_name = db.query(Classes).get(class_id).class_name.split(" ")[-1]
    section_name = db.query(Sections).get(section_id).section_name.split(" ")[-1]
    last_roll_number = db.query(Student).filter(
        Student.class_id == class_id,
        Student.section_id == section_id,
        Student.institute_id == institute_id
    ).order_by(Student.student_id.desc()).first()

    if last_roll_number is None:
        last_roll_number = 1
    else:
        # Extract the roll number from the last_roll_number object
        last_roll_number = int(last_roll_number.roll_number.split('-')[-1])

    roll_number = f"{institute_id}-{class_name}-{section_name}-{last_roll_number + 1}"

    # Ensure the generated roll number is unique
    while db.query(Student).filter(Student.roll_number == roll_number).first():
        last_roll_number += 1
        roll_number = f"{institute_id}-{class_name}-{section_name}-{last_roll_number}"

    return roll_number

# geting all student according to institute id
@router.get("/get_students_by_intitute/",description="get all the students by institute id")
async def get_all_students( institute_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    students = ModelManager.get_student_data_by_institute(db.query(Student),institute_id)
    return jsonable_encoder(students)

@router.get("/get_students_by_field/{field_name}/{field_value}/")
async def get_all_students_by_field(field_name:str,field_value:str,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    student_model = Student
    students = ModelManager.get_data_by_field(db.query(student_model),field_name,field_value,student_model)
    return jsonable_encoder(students)



# creating student data
@router.post("/create_student/")
async def create_student(student: StudentBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        # Create a new Student instance with the provided data
        new_student = Student(**student.dict())
        new_student.slug = generate_slug(student.student_name,db)
        new_student.roll_number = generate_roll_number(student.class_id,student.section_id,student.institute_id,db)
        # Add, commit, and refresh the new student
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        # Fetch the new student data, including foreign keys' names
        new_student_with_names = db.query(Student).filter(Student.student_id == new_student.student_id).first()
        # Convert foreign keys' names to IDs
        new_student_with_names.class_id = db.query(Classes).get(new_student_with_names.class_id).class_name
        new_student_with_names.section_id = db.query(Sections).get(new_student_with_names.section_id).section_name
        if db.query(Transport).get(new_student_with_names.transport_id):
            new_student_with_names.transport_id = db.query(Transport).get(new_student_with_names.transport_id).transport_name
        return succes_response(new_student_with_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")



# updating student data
@router.put("/update_student/{student_id}")
async def update_student(student_id: int, student: StudentBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
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
async def get_student_data_by_id(student_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        return succes_response(student_data)
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# deleteing the students
@router.delete("/delete_student/")
async def delete_student(student_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        student_id = student_data.student_id
        db.delete(student_data)
        db.commit()
        return {"status": "200", "msg": "done", 'response':student_id}
    else:
        raise HTTPException(status_code=404, detail="Student not found")