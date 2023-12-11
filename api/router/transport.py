from datetime import date
import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field,ValidationError
from models import transports
tbl_transports = transports.Transport
from .database_connnection import get_db
from database import engine
transports.BASE.metadata.create_all(bind = engine)
from sqlalchemy.orm import Session
router = APIRouter()

# base schema
class TransportBase(BaseModel):
    institute_id:int
    transport_name : str = Field(min_length=3)
    vehicle_number : str = Field(min_length=3)
    vehicle_details : Optional[str]
    register_date : date = Field(default_factory=date.today)
 
class StopsBase(BaseModel):
    stop_name : str = Field(min_length=3)
    transport_id : int

@router.post("/create_transport/")
async def create_transport(trans_data:TransportBase,db:Session = Depends(get_db)):
    try:
        trans_instnace = tbl_transports(**trans_data.dict())
        db.add(trans_instnace)
        db.commit()
        db.refresh(trans_instnace)
        return {
            "status_code": 200,
            "msg": "done",
            "response": trans_instnace
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
@router.get("/get_all_transports/")
async def get_all_transports(db:Session = Depends(get_db)):
    return jsonable_encoder(db.query(tbl_transports).all())
