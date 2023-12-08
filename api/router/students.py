from datetime import date
import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
import models
from .database_connnection import get_db,SessionLocal
from database import engine
models.BASE.metadata.create_all(bind = engine)
from sqlalchemy.orm import Session
router = APIRouter()

class StudentBase(BaseModel):
    first_name:str = Field(min_length=3,max_length=20)
    last_name: Optional[str]
    age: int = Field(gt=2)
    date_of_birth :date = Field(default_factory=date.today)
    blood_group: str = Field(min_length=2)
    address :str = Field(min_length=3,max_length=20)
    email :str = Field(min_length=5)
    phone_number :str = Field (min_length=10,max_length=10)

@router.get("/")
async def get_all_students(db:Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return jsonable_encoder(students)

@router.post("/")
async def create_student(student:StudentBase,db:Session = Depends(get_db)):
    try:
        new_student = models.Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"statu":"200","msg":"done",'response':new_student}
    except:
        raise HTTPException(status_code=400,detail="Error in creating student")
    
@router.put("/{student_id}")
async def update_student(student_id: int, student: StudentBase, db: Session = Depends(get_db)):
    # Use .first() to execute the query and retrieve the first result
    student_data = db.query(models.Student).filter(models.Student.id == student_id).first()
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
    student_data = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_data is not None:
        return {"status":"200","msg":"done",'response':student_data}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{student_id}")
async def delete_student(student_id:int,db:Session = Depends(get_db)):
    student_data = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_data is not None:
        student_id = student_data.id
        db.delete(student_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"student_id":student_id}}
    else:
        raise HTTPException(status_code=404, detail="Student not found")

