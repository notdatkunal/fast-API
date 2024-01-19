from datetime import date, timedelta
import sys
sys.path.append("..")
from router.basic_import import *
from router.utility import succes_response
from pydantic import BaseModel
from models.students import Student
from models.fees import studentDiscount,StudentInstallemnt,\
fees_installments_association,Fees,ClassInstallment
from sqlalchemy.orm import contains_eager

router = APIRouter()

# base models
class StudentFeeBase(BaseModel):
    student_id: int
    fee_total: float
    discount: float
    intstall_count: int

# create Student Discount
async def create_student_discount(db=None,student_id:int=None,discount:float=None):
    try:
        student_discount = studentDiscount(student_id=student_id,discount=discount)
        db.add(student_discount)
        db.commit()
        db.refresh(student_discount)
        return "Student Discount Created Successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def genarete_student_fee(db=None,student_id:int=None,fee_total:float=None,discount:float=None,install_count:int=None):
    data = []
    for i in range(1,install_count+1):
        student_fee = StudentInstallemnt()
        student_fee.student_id = student_id
        student_fee.installment_name = f"installment_{i}"
        student_fee.installment_amount = round(fee_total/install_count,2)
        student_fee.installment_due_date = date.today()+timedelta(days=30*i)
        student_fee.installment_status = False
        student_fee.installment_paid_date = None
        data.append(student_fee)
    db.bulk_save_objects(data)
    db.commit()
    return "Student Fee Generated Successfully"

@router.post("/create_student_fee/")
async def post_student_fee(student_fee:StudentFeeBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
    student = db.query(Student).filter(Student.student_id == student_fee.student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    is_fee_created = db.query(StudentInstallemnt).filter(StudentInstallemnt.student_id == student_fee.student_id).first()
    if is_fee_created is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Student Fee Already Created")
    try:
        student_id = student.student_id
        fee_total = student_fee.fee_total
        discount = student_fee.discount
        install_count = student_fee.intstall_count
        await create_student_discount(db,student_id,discount)
        await genarete_student_fee(db,student_id,fee_total,discount,install_count)
        return succes_response("Student Fee Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all_student_installments/")
async def get_all_student_installments(student_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    class_id = (db.query(Student).filter(Student.student_id == student_id).first()).class_id
    fee_data = (
            db.query(Fees)
            .join(fees_installments_association)
            .join(ClassInstallment)
            .filter(Fees.class_id == class_id)
            .options(contains_eager(Fees.class_installments))
            .all()
        )
    try:
        student_fee = (
            db.query(StudentInstallemnt)
            .filter(StudentInstallemnt.student_id == student_id)
            .all()
        )
        discount = (
            db.query(studentDiscount)
            .filter(studentDiscount.student_id == student_id)
            .first()
        )
        payload = {
            "fee_data":fee_data,
            "student_fee":student_fee,
            "discount":discount
        }
        return jsonable_encoder(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# current_user: str = Depends(is_authenticated)
    
# delete all installments of students
@router.delete("/delete_all_student_installments/")
async def delete_all_student_installments(student_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        db.query(StudentInstallemnt).filter(StudentInstallemnt.student_id == student_id).delete()
        db.commit()
        return succes_response("Student Installments Deleted Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update_student_installment/")
async def update_student_installment(installment_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    installment = db.query(StudentInstallemnt).filter(StudentInstallemnt.installment_id == installment_id).first()
    if installment is None:
        raise HTTPException(status_code=404, detail="Installment not found")
    try:
        installment.installment_status = True
        installment.installment_paid_date = date.today().strftime("%d-%m-%Y")
        db.commit()
        db.refresh(installment)
        return succes_response(data=installment,msg="Installment Updated Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

