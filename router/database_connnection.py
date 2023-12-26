from database import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
def get_db():
    print("db_started")
    db = SessionLocal()
    try:
        print("db_connection")
        yield db
    finally:
        print("db_closed")
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]