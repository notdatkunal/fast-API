from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.staffs import Staff,Staff_Payroll as staff_payroll_data
from router.utility import succes_response

router = APIRouter()

class StaffBase(BaseModel):
    institute_id: int
    employee_id: int
    staff_name: str = Field(..., min_length=3, max_length=30)
    photo: Optional[str]
    role: Optional[str] = None  
    address: Optional[str]
    gender: Optional[str] = Field(None, min_length=2)  
    experience: Optional[str]
    specialization: Optional[str]
    phone_number: str = Field(..., min_length=10)
    email: str
    blood_group: Optional[str]
    date_of_birth: Optional[date] = Field(default_factory=date.today)
    joining_date: Optional[date] = Field(default_factory=date.today)
    salary: Optional[str]
    slug: Optional[str]
    is_deleted: Optional[bool] = False  
    
    # foreign keys
    transport_id: Optional[int] = None
    
class StaffPayrollBase(BaseModel):
    staff_id: int
    payroll_type: Optional[str]
    salary_amount: Optional[str]
    payment_date: Optional[date] = Field(default_factory=date.today)
    payment_mode: Optional[str]
    payroll_details: Optional[str]

@router.get("/get_staffs_by_institute/")
async def get_all_staffs(institute_id:int,db:Session = Depends(get_db)):
    staffs_model = Staff
    staffs = ModelManager.get_data_by_institute(db.query(Staff),staffs_model,institute_id)
    return jsonable_encoder(staffs)

@router.get("/get_staffs_by_field/{field_name}/{field_value}/")
async def get_all_staffs_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    staff_model = Staff
    staffs = ModelManager.get_data_by_field(db.query(staff_model),field_name,field_value,staff_model)
    return jsonable_encoder(staffs)


@router.post("/create_staff/")
async def create_staff(staff:StaffBase,db:Session = Depends(get_db)):
    try:
        new_staff = Staff(**staff.dict())
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return succes_response(new_staff)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
@router.put("/update_staff/")
async def update_staff(staff_id: int, staff: StaffBase, db: Session = Depends(get_db)):
    staff_data = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff_data is not None:
        for key, value in staff.dict(exclude_unset=True).items():
            setattr(staff_data, key, value)
        db.commit()
        db.refresh(staff_data)
        return succes_response(staff_data)
    else:
        raise HTTPException(status_code=404, detail="Staff not found")


@router.get("/get_staff_by_id/")
async def get_staff_data_by_id(staff_id:int,db:Session = Depends(get_db)):
    staff_data = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff_data is not None:
        return {"status":"200","msg":"done",'response':staff_data}
    else:
        raise HTTPException(status_code=404, detail="Staff not found")

 
@router.delete("/delete_staff/") 
async def delete_staff(staff_id:int,db:Session = Depends(get_db)):
    staff_data = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff_data is not None:
        staff_id = staff_data.staff_id
        db.delete(staff_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"staff_id":staff_id}}
    else:
        raise HTTPException(status_code=404, detail="Staff not found")


