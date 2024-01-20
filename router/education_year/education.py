from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.education import EducationYear
from models.institute import Institute
from router.utility import succes_response
router = APIRouter()

# base models
class EducationYearBase(BaseModel):
    institute_id:int
    education_year_name:str
    education_year_start_date: date =Field(default_factory=date.today)
    education_year_end_date : date =Field(default_factory=date.today)
    is_active: bool = False

# post education year
@router.post("/create_education_year/")
async def create_education_year(education_year:EducationYearBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    if db.query(Institute).filter(Institute.id == education_year.institute_id).first() is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    try:
        education_year_instance = EducationYear(**education_year.dict())
        db.add(education_year_instance)
        db.commit()
        db.refresh(education_year_instance)
        return succes_response(education_year_instance,msg="Education Year Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# get education year by institute id
@router.get("/get_education_year_by_institute_id/")
async def get_education_year_by_institute_id(institute_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    institute = db.query(Institute).filter(Institute.id == institute_id).first()
    if institute is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    try:
        education_year = db.query(EducationYear).filter(EducationYear.institute_id == institute_id).all()
        return succes_response(education_year,msg="Education Year Found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No ID Found")

# get education year by id
@router.get("/get_education_year_by_id/")
async def get_education_year_by_id(education_year_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    education_year = db.query(EducationYear).filter(EducationYear.education_year_id == education_year_id).first()
    if education_year is None:
        raise HTTPException(status_code=404, detail="Education Year not found")
    try:
        return succes_response(education_year,msg="Education Year Found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No ID Found")

# update education year by id
@router.patch("/update_education_year/")
async def update_education_year(education_year_id:int,education_year:EducationYearBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    education_year_instance = db.query(EducationYear).filter(EducationYear.education_year_id == education_year_id).first()
    if education_year_instance is None:
        raise HTTPException(status_code=404, detail="Education Year not found")
    try:
        education_year_instance.education_year_name = education_year.education_year_name
        education_year_instance.education_year_start_date = education_year.education_year_start_date
        education_year_instance.education_year_end_date = education_year.education_year_end_date
        db.commit()
        db.refresh(education_year_instance)
        return succes_response(education_year_instance,msg="Education Year Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No ID Found")

# activate education year by id
@router.patch("/activate_education_year/")
async def activate_education_year(education_year_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    education_year_instance = db.query(EducationYear).filter(EducationYear.education_year_id == education_year_id).first()
    if education_year_instance is None:
        raise HTTPException(status_code=404, detail="Education Year not found")
    try:
        education_year_instance.is_active = True
        education_year = db.query(EducationYear).filter(EducationYear.institute_id == education_year_instance.institute_id).all()
        for year in education_year:
            if year.education_year_id != education_year_id:
                year.is_active = False
        db.commit()
        db.refresh(education_year_instance)
        return succes_response(education_year_instance,msg="Education Year Activated Successfully")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No ID Found")

# delete education year by id
@router.delete("/delete_education_year/")
async def delete_education_year(education_year_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    education_year_instance = db.query(EducationYear).filter(EducationYear.education_year_id == education_year_id).first()
    if education_year_instance is None:
        raise HTTPException(status_code=404, detail="Education Year not found")
    try:
        db.delete(education_year_instance)
        db.commit()
        return succes_response(msg="Education Year Deleted Successfully")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No ID Found")


