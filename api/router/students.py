from datetime import date
import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
from models import *
from .database_connnection import get_db,SessionLocal
from database import engine
students.BASE.metadata.create_all(bind = engine)
from sqlalchemy.orm import Session
router = APIRouter()

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
    transport_id :int

@router.get("/")
async def get_all_students(db:Session = Depends(get_db)):
    students = db.query(Student).all()
    return jsonable_encoder(students)

@router.post("/")
async def create_student(student:StudentBase,db:Session = Depends(get_db)):
    try:
        new_student = Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"statu":"200","msg":"done",'response':new_student}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
@router.put("/{student_id}")
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


@router.get("/student_id")
async def get_student_data_by_id(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        return {"status":"200","msg":"done",'response':student_data}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{student_id}")
async def delete_student(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(Student).filter(Student.student_id == student_id).first()
    if student_data is not None:
        student_id = student_data.student_id
        db.delete(student_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"student_id":student_id}}
    else:
        raise HTTPException(status_code=404, detail="Student not found")

