import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException
from database import engine
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
from models import *
from models.classes import Classes,Sections,Subjects
from .database_connnection import get_db
from sqlalchemy.orm import Session
classes.BASE.metadata.create_all(bind = engine)
router = APIRouter()
# base models
class ClassBase(BaseModel):
    class_name : str = Field(min_length=3)
    slug:str
    is_deleted: bool = Field(default=False)
    institute_id:int
class SectionBase(BaseModel):
    section_name : str = Field(min_length=3)
    is_deleted :bool = Field(default=False)
    class_id :int
class SubjectBase(BaseModel):
    subject_name : str = Field(min_length=3)
    class_id :int

# createing class
@router.post("/create_class/")
async def create_class(class_data: ClassBase, db: Session = Depends(get_db)):
    try:
        class_instance = Classes(**class_data.dict())
        db.add(class_instance)
        db.commit()
        db.refresh(class_instance)
        payload = succes_response(class_instance)
        return payload
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")


@router.get("/get_all_classes/")
async def get_all_classes(db:Session = Depends(get_db)):
    classes_obj = db.query(Classes).filter(Classes.is_deleted == False).all()
    return jsonable_encoder(classes_obj)

@router.post("/create_section/")
async def create_section_for_class(section_data:SectionBase,db:Session = Depends(get_db)):
    try:
        section_instance = Sections(**section_data.dict())
        db.add(section_instance)
        db.commit()
        db.refresh(section_instance)
        payload = succes_response(section_instance)
        return payload
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/get_all_sections/")
async def get_all_sections(db:Session = Depends(get_db)):
    return jsonable_encoder(db.query(Sections).all())

@router.get("/get_sections_by_class/")
async def get_sections_by_class(class_id:int,db:Session = Depends(get_db)):
    class_instance = db.query(Classes).filter(Classes.class_id == class_id).first()
    if class_instance:
        sections = db.query(Sections).filter(Sections.class_id == class_id).all()
        return jsonable_encoder(sections)
    else:
        return HTTPException(status_code=404,detail="Class not found")
def succes_response(data):
    return {
            "status_code": 200,
            "msg": "done",
            "response": data
        }
