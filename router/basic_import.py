from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,HTTPException
from database import engine,SessionLocal
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
from .database_connnection import get_db
from sqlalchemy.orm import Session