from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.staffs import Staff_Payroll as staff_payroll_data
from router.utility import succes_response

router = APIRouter()

# base model
class StaffPayrollBase(BaseModel):
    staff_id: int
    payroll_type: Optional[str]
    salary_amount: Optional[str]
    payment_date: Optional[date] = Field(default_factory=date.today)
    payment_mode: Optional[str]
    payroll_details: Optional[str]

@router.post("/add_payroll/")
async def create_payroll(payroll:StaffPayrollBase, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        new_payroll = staff_payroll_data(**payroll.dict())
        db.add(new_payroll)
        db.commit()
        db.refresh(new_payroll)
        return succes_response(new_payroll,msg="Payroll Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")


@router.get("/get_payroll_data_by_staff/")
async def get_payroll_data_by_id(staff_id:int, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    payroll_data = db.query(staff_payroll_data).filter(staff_payroll_data.staff_id == staff_id).all()
    if payroll_data is not None:
        return succes_response(payroll_data)
    else:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
@router.get("/get_payroll_by_id/")
async def get_payroll(payroll_id:int, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    payroll_data = db.query(staff_payroll_data).filter(staff_payroll_data.payroll_id == payroll_id).first()
    if payroll_data is not None:
        return succes_response(payroll_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")

@router.put("/update_payroll/")
async def update_staff(payroll_id: int, staff: StaffPayrollBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    payroll_data = db.query(staff_payroll_data).filter(staff_payroll_data.payroll_id == payroll_id).first()
    if payroll_data is not None:
        for key, value in staff.dict(exclude_unset=True).items(): 
            setattr(payroll_data, key, value)
        db.commit()
        db.refresh(payroll_data)
        return succes_response(payroll_data,msg="Payroll Updated Successfully")
    else:
        raise HTTPException(status_code=404, detail="Payroll not found")


@router.delete("/delete_payroll/")
async def delete_staff(payroll_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    payroll_data = db.query(staff_payroll_data).filter(staff_payroll_data.payroll_id == payroll_id).first()
    if payroll_data is not None:
        staff_id = payroll_data.staff_id
        db.delete(payroll_data)
        db.commit()
        return succes_response({"staff_id":staff_id},msg="Payroll Deleted Successfully")
    else:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
