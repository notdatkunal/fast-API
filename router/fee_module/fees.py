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
    total_installments:float
    installment_id:List[int]


# base models of installment
class InstallmentBase(BaseModel):
    installment_name: str
    installment_number: int

def create_association_bulk(fee_id, installment_ids, db):
    try:
        # Create a list of dictionaries for bulk insert
        for ele in installment_ids:
            association_data = {"fee_id": fee_id, "installment_id": ele}
            db.execute(
                fees_installments_association.insert().values(association_data)
            )
            db.commit()
        return {"status": "Associations created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating associations: {e}")
    
def update_association(fee_id, installment_ids, db):
    try:
        # Delete all the existing associations
        db.query(fees_installments_association).filter(
            fees_installments_association.c.fee_id == fee_id
        ).delete(synchronize_session=False)
        # Create a list of dictionaries for bulk insert
        for ele in installment_ids:
            association_data = {"fee_id": fee_id, "installment_id": ele}
            db.execute(
                fees_installments_association.insert().values(association_data)
            )
            db.commit()
        return {"status": "Associations updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating associations: {e}")
    
def get_fee_data(fee, db):
    fee_instance = (
        db.query(Fees)
        .join(fees_installments_association)
        .join(ClassInstallment)
        .join(Classes, Classes.class_id == fee.class_id) 
        .options(contains_eager(Fees.class_installments))
        .options(contains_eager(Fees.class_fees))
        .filter(Fees.fee_id == fee.fee_id)
        .all()
    )
    return fee_instance


# create fees
@router.post("/create_fees/")
async def create_fees(fees:FeesBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    institute = db.query(Institute).filter(Institute.id == fees.institution_id).first()
    if institute is None:
        raise HTTPException(status_code=404, detail="Institute not found")
    if db.query(Classes).filter(Classes.class_id == fees.class_id,Classes.institute_id== institute.id).first() is None:
        raise HTTPException(status_code=404, detail="Class not found OR Class not belongs to this institute")

    if db.query(ClassInstallment).filter(ClassInstallment.installment_id.in_(fees.installment_id)).first() is None:
        raise HTTPException(status_code=404, detail="Installment not found")
    
    try:
        new_fees = Fees()
        new_fees.institution_id = fees.institution_id
        new_fees.class_id = fees.class_id
        new_fees.fee_total = fees.fee_total
        new_fees.fee_admission = fees.fee_admission
        new_fees.total_installments = fees.total_installments
        db.add(new_fees)
        db.commit()
        db.refresh(new_fees)
        create_association_bulk(new_fees.fee_id, fees.installment_id, db)
        fee_instance = get_fee_data(new_fees,db)
        return succes_response(jsonable_encoder(fee_instance),msg="Fees Created Successfully")
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
        new_installment = db.query(ClassInstallment).filter(ClassInstallment.installment_id == new_installment.installment_id).first()
        return succes_response(jsonable_encoder(installment),msg="Installment Created Successfully")
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
                db.query(Fees)
                .join(fees_installments_association)
                .join(ClassInstallment)
                .options(contains_eager(Fees.class_installments))
                .all()
            )
        # Convert the result to a list of dictionaries
        fees_data = jsonable_encoder(fees_obj)
        return fees_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fees: {e}")

# get all fees by institute id
@router.get("/get_all_fees_by_institute/")
async def get_all_fees_by_institute(institution_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        fees_obj = (
                db.query(Fees)
                .join(fees_installments_association)
                .join(ClassInstallment)
                .join(Classes,Fees.class_id == Classes.class_id)
                .filter(Fees.institution_id == institution_id)
                .options(contains_eager(Fees.class_installments))
                .options(contains_eager(Fees.class_fees))
                .all()
            )
        # Convert the result to a list of dictionaries
        fees_data = jsonable_encoder(fees_obj)
        return fees_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fees: {e}")
    
# get all fees by class id
@router.get("/get_all_fees_by_class/")
async def get_all_fees_by_class(class_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        fees_objs = (
            db.query(Fees)
            .join(fees_installments_association)
            .join(ClassInstallment)
            .filter(Fees.class_id == class_id)
            .options(contains_eager(Fees.class_installments))
            .all()
        )
        return jsonable_encoder(fees_objs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fees: {e}")
    
# get fee by id
@router.get("/get_fee_by_id/")
async def get_fee_by_id(fee_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        fees_obj = (
            db.query(Fees)
            .join(fees_installments_association)
            .join(ClassInstallment)
            .join(Classes)
            .filter(Fees.fee_id == fee_id)
            .options(contains_eager(Fees.class_installments))
            .options(contains_eager(Fees.class_fees))
            .all()
        )
        return succes_response(fees_obj,msg="Fee Found Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fees: {e}")

# update fees
@router.put("/update_fees/")
async def update_fee(fee_id:int,fees:FeesBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    fee_obj = db.query(Fees).filter(Fees.fee_id == fee_id).first()
    if fee_obj is None:
        raise HTTPException(status_code=404, detail="Fee not found")
    class_obj = db.query(Classes).filter(Classes.class_id == fees.class_id).first()
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_obj.institute_id != fees.institution_id:
        raise HTTPException(status_code=404, detail="Class not belongs to this institute")
    try:
        for key, value in fees.dict(exclude_unset=True).items(): 
            setattr(fee_obj, key, value)
        db.commit()
        db.refresh(fee_obj)
        update_association(fee_obj.fee_id, fees.installment_id, db)
        fee_instance = get_fee_data(fee_obj,db)
        return succes_response(fee_instance,msg="Fee Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

# delete fees
@router.delete("/delete_fees/")
async def delete_fee(fee_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    fee_obj = db.query(Fees).filter(Fees.fee_id == fee_id).first()
    if fee_obj is None:
        raise HTTPException(status_code=404, detail="Fee not found")
    db.delete(fee_obj)
    db.commit()
    return succes_response("",msg="Fee Deleted Successfully")
    




