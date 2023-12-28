from datetime import date
import sys
from models.staffs import Staff
sys.path.append("..")
from router.basic_import import *
from models.transports import Transport
from router.utility import succes_response
from models.students import Student

router = APIRouter()
tbl_transports = Transport
# base schema
class TransportBase(BaseModel):
    institute_id:int
    transport_name : str = Field(min_length=3)
    vehicle_number : str = Field(min_length=3)
    vehicle_details : Optional[str]
    register_date : date = Field(default_factory=date.today)

# post  api  for transport
@router.post("/create_transport/",description="create transport",status_code=201)
async def create_transport(trans_data:TransportBase,db:db_dependency,current_user: str = Depends(is_authenticated)):
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
    


    # get api  code for transportation
@router.get("/get_all_transports/",description="get all transport",status_code=200)
async def get_all_transports(db:db_dependency,current_user: str = Depends(is_authenticated)):
    return jsonable_encoder(db.query(tbl_transports).all())


# update api code for  transpotation 
@router.put("/update_transport/",description="update transport Here",status_code=200)
async def update_transport(transport_id: int, transport: TransportBase, db: db_dependency,current_user: str = Depends(is_authenticated)):
    # Use .first() to execute the query and retrieve the first result
    transpotation_data = db.query(tbl_transports).filter(tbl_transports.transport_id == transport_id).first()
    if  transpotation_data  is not None:
        for key, value in transport.dict(exclude_unset=True).items():
            setattr(transpotation_data , key, value)
        db.commit()
        db.refresh(transpotation_data )
        return {"status":"200","msg":"done",'response': transpotation_data }
    else:
        raise HTTPException(status_code=404, detail="transport not found")
    
@router.get("/get_transport_data_by_id/",description="Get Transport by using ID",status_code=200)
async def get_transport_data_by_id(transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    transport_details = db.query(tbl_transports).filter(tbl_transports.transport_id == transport_id).first()
    if transport_details is not None:
        return {"status":"200","msg":"done",'response':transport_details}
    else:
        raise HTTPException(status_code=404, detail="transpotation  not found")

# delete api code for  transpotation
@router.delete("/delete_transport/",description="delete transport",status_code=200)
async def delete_transport(transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    transport_data = db.query(tbl_transports).filter(tbl_transports.transport_id == transport_id).first()
    if transport_data is not None:
        transport_id = transport_data.transport_id
        db.delete(transport_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"transport_id":transport_id}}
    else:
        raise HTTPException(status_code=404, detail="transport not found")
    

# assigning student to transport
@router.put("/assign_transport_to_student/",description="assign transport to student",status_code=200)
async def assign_student_to_transport(student_roll_number:str,transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    transport = db.query(Transport).filter(Transport.transport_id == transport_id).first()
    if transport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    try:
        student_data = db.query(Student).filter(Student.roll_number == student_roll_number).first()
        if student_data is not None:
            student_data.transport_id = transport_id
            db.commit()
            db.refresh(student_data)
            return succes_response(student_data)
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# assigning transport to student
@router.put("/assign_transport_to_staff/",description="assign transport to staff",status_code=200)
async def assign_transport_to_staff(employee_id:str,transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    transport = db.query(Transport).filter(Transport.transport_id == transport_id).first()
    if transport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    try:
        staff = db.query(Staff).filter(Staff.employee_id == employee_id).first()
        if staff is not None:
            staff.transport_id = transport_id
            db.commit()
            db.refresh(staff)
            return succes_response(staff)
        else:
            raise HTTPException(status_code=404, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# unassigning transport to student
@router.put("/unassign_transport_to_student/",description="unassign transport to student",status_code=200)
async def unassign_student_to_transport(student_roll_number:str,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        student_data = db.query(Student).filter(Student.roll_number == student_roll_number).first()
        if student_data is not None:
            student_data.transport_id = None
            db.commit()
            db.refresh(student_data)
            return succes_response(student_data)
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    
# unassigning transport to staff
@router.put("/unassign_transport_to_staff/",description="unassign transport to staff",status_code=200)
async def unassign_transport_to_staff(employee_id:str,db:db_dependency,current_user: str = Depends(is_authenticated)):
    try:
        staff = db.query(Staff).filter(Staff.employee_id == employee_id).first()
        if staff is not None:
            staff.transport_id = None
            db.commit()
            db.refresh(staff)
            return succes_response(staff)
        else:
            raise HTTPException(status_code=404, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")
    

# geting all students by transport id
@router.get("/get_all_students_by_transport_id/",description="get all students by transport id",status_code=200)
async def get_all_students_by_transport(transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    trasport = db.query(Transport).filter(Transport.transport_id == transport_id).first()
    if trasport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    try:
        students = db.query(Student).filter(Student.transport_id == transport_id).order_by(Student.roll_number).all()
        if students is not None:
            return succes_response(students)
        else:
            raise HTTPException(status_code=404, detail="Students not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Geting data: {str(e)}") 

# geting all staffs by transport id
@router.get("/get_all_staffs_by_transport_id/",description="get all staffs by transport id",status_code=200)
async def get_all_staffs_by_transport(transport_id:int,db:db_dependency,current_user: str = Depends(is_authenticated)):
    trasport = db.query(Transport).filter(Transport.transport_id == transport_id).first()
    if trasport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    try:
        staffs = db.query(Staff).filter(Staff.transport_id == transport_id).order_by(Staff.employee_id).all()
        if staffs is not None:
            return succes_response(staffs)
        else:
            raise HTTPException(status_code=404, detail="Staffs not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Geting data: {str(e)}") 
