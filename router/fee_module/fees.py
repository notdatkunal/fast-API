from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from router.utility import succes_response
from models.fees import Fees,ClassInstallment,fees_installments_association
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager
from models.institute import Institute
from models.classes import Classes

router = APIRouter()
# base models
class FeesBase(BaseModel):
    institution_id: int
    class_id: int
    fee_total: float
    fee_admission: float
    installment_id: int

    class Config:
        orm_mode = True

# base models of installment
class InstallmentBase(BaseModel):
    installment_name: str
    installment_number: int

    class Config:
        orm_mode = True


def create_association(fee_id, installment_id, db):
    try:
        # Insert into the association table
        db.execute(
            fees_installments_association.insert().values(
                fee_id=fee_id,
                installment_id=installment_id
            )
        )
        db.commit()
        return {"status": "Association created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating association: {e}")

# create fees
@router.post("/create_fees/")
async def create_fees(fees:FeesBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    institute = db.query(Institute).filter(Institute.id == fees.institution_id).first()
    if institute is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    if db.query(Classes).filter(Classes.class_id == fees.class_id,Classes.institute_id== institute.id).first() is None:
        raise HTTPException(status_code=404, detail="Class not found OR Class not belongs to this institute")
    if db.query(ClassInstallment).filter(ClassInstallment.installment_id == fees.installment_id).first() is None:
        raise HTTPException(status_code=404, detail="Installment not found")
    try:
        new_fees = Fees()
        new_fees.institution_id = fees.institution_id
        new_fees.class_id = fees.class_id
        new_fees.fee_total = fees.fee_total
        new_fees.fee_admission = fees.fee_admission
        db.add(new_fees)
        db.commit()
        db.refresh(new_fees)
        create_association(new_fees.fee_id, fees.installment_id, db)
        return succes_response(jsonable_encoder(fees))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# create installment
@router.post("/create_installment/")
async def create_installment(installment:InstallmentBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        new_installment = ClassInstallment(**installment.dict())
        db.add(new_installment)
        db.commit()
        db.refresh(new_installment)
        return succes_response(jsonable_encoder(installment))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# get all installments
@router.get("/get_all_installments/")
async def get_all_installments(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        installment_obj = db.query(ClassInstallment).all()
        # Convert the result to a list of dictionaries
        installment_data = jsonable_encoder(installment_obj)
        return installment_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving installment: {e}")
    
# get all fees
@router.get("/get_all_fees/")
async def get_all_fees(db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        fees_obj = (
                db.query(Fees).
                join(fees_installments_association)
                .join(ClassInstallment)
                .options(contains_eager(Fees.class_installments))
                .all()
            )
        # Convert the result to a list of dictionaries
        fees_data = jsonable_encoder(fees_obj)
        return fees_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fees: {e}")
    




