from datetime import date
import random
import sys
import uuid
sys.path.append("..")
from router.basic_import import *
from models.students import Student
from models import Classes,Transport,Sections
from models.manager import ModelManager
from router.utility import succes_response
router = APIRouter()
from faker import Faker
fake = Faker()

# student base model
class StudentBase(BaseModel):
    institute_id :int
    student_name :str = Field(min_length=3,max_length=30)
    gender :str = Field(min_length=2)
    date_of_birth :date = Field(default_factory=date.today)
    blood_group :str
    roll_number :str
    address :Optional[str]
    phone_number :str = Field(min_length=10,max_length=10)
    email :Optional[str]
    admission_date :date
    photo :str
    # foreign keys
    class_id :int
    section_id :int

def get_student_filter_query(db=None,filter_column:str=None,filter_value:str=None):
    try:
        student_data = (
            db.query(Student)
            .join(Classes, Student.class_id == Classes.class_id)
            .join(Sections, Student.section_id == Sections.section_id)
            .options(joinedload(Student.classes).load_only(Classes.class_name))
            .options(joinedload(Student.sections).load_only(Sections.section_name))
            .filter(getattr(Student,filter_column) == filter_value)
            .all()
        )
        return student_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# genarating slug using student name and student class
def generate_slug(student_name:str,db):
    slug = student_name.replace(" ","-")
    while True:
        if db.query(Student).filter(Student.slug == slug).first():
            slug = slug + str(uuid.uuid4())[:6]
        else:
            return slug

# geting all student according to institute id
@router.get("/get_students_by_intitute/",description="get all the students by institute id")
async def get_all_students( institute_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    student_data = get_student_filter_query(db,"institute_id",institute_id)
    return jsonable_encoder(student_data)

# geting all student according to institute id
@router.get("/get_students_by_field/{field_name}/{field_value}/")
async def get_all_students_by_field(field_name:str,field_value:str,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    students = get_student_filter_query(db,field_name,field_value)
    return jsonable_encoder(students)

# creating student data
@router.post("/create_student/")
async def create_student(student: StudentBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        # Create a new Student instance with the provided data
        new_student = Student(**student.dict())
        new_student.slug = generate_slug(student.student_name,db)
        # Add, commit, and refresh the new student
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        student_data = get_student_filter_query(db,"student_id",new_student.student_id)
        return succes_response(student_data,msg="Student Created Successfully")
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
        student_data = get_student_filter_query(db,"student_id",student_id)
        return succes_response(student_data,msg="Student Updated Successfully")
    else:
        raise HTTPException(status_code=404, detail="Student not found")


# geting student data by id
@router.get("/get_student/")
async def get_student_data_by_id(student_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        return succes_response(get_student_filter_query(db,"student_id",student_id))
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
        return succes_response(student_id,msg="Student Deleted Successfully")
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    

def rand_class_id(institute_id:int,db):
    class_data = db.query(Classes).filter(Classes.institute_id == institute_id).all()
    class_id  = random.choice(class_data).class_id
    sections = db.query(Sections).filter(Sections.class_id == class_id).all()
    if sections:
        section_id = random.choice(sections).section_id
    else:
        section_id =  1
    return class_id,section_id

@router.get("/create_fake_students/")
async def create_fake(institute_id:int,range_:int,db:db_dependency):
    for _ in range(range_):
        class_id,section_id = rand_class_id(institute_id,db)
        student = StudentBase(
            institute_id=institute_id,
            student_name=fake.name(),
            gender=random.choice(["Male","FeMale"]),
            date_of_birth=fake.date(),
            blood_group=random.choice(["A+","A-","B+","B-","AB+","AB-","O+","O-"]),
            roll_number=f"{institute_id}-{_}",
            address=fake.address(),
            phone_number=''.join(["{}".format(random.randint(0, 9)) for num in range(0, 10)]),
            email=fake.email(),
            admission_date=fake.date(),
            photo="",
            class_id=class_id,
            section_id=section_id
        )
        new_student = Student(**student.dict())
        new_student.slug = generate_slug(student.student_name,db)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    return {"msg":"fake students created successfully"}



    
