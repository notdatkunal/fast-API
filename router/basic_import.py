from typing import Optional,List,Dict
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,HTTPException,status
from database import engine,SessionLocal
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
from router.database_connnection import get_db,db_dependency
from sqlalchemy.orm import Session
from models.manager import ModelManager
from .users.login import get_current_user
from sqlalchemy.orm import joinedload,Load,load_only,contains_eager
from sqlalchemy.exc import SQLAlchemyError

def is_authenticated(current_user: str = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user
