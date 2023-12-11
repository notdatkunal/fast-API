import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field,ValidationError
from models import *
from .database_connnection import get_db
from database import engine
institute.BASE.metadata.create_all(bind = engine)
from sqlalchemy.orm import Session
router = APIRouter()


class InstituteSchema(BaseModel):
    name :str = Field(max_length=20)
    address :Optional[str]
    city :Optional[str]
    state :Optional[str]
    country :Optional[str]
    pincode :Optional[str]
    phone :str = Field(max_length=10,min_length=10)
@router.get("/")
async def get_all_institutes(db:Session =Depends(get_db)):
    all_institutes = db.query(Institute).all()
    return jsonable_encoder(all_institutes)

@router.post("/")
async def create_institute(institute:InstituteSchema,db:Session = Depends(get_db)):
    new_institute = Institute
    db.add(new_institute(**institute.__dict__))
    db.commit()
    return {"msg":"Institute is Saved"}
