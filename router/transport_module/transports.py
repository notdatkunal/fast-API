from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.transports import Transport
from router.utility import succes_response

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
@router.post("/create_transport/")
async def create_transport(trans_data:TransportBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
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
@router.get("/get_all_transports/")
async def get_all_transports(db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    return jsonable_encoder(db.query(tbl_transports).all())


# update api code for  transpotation 
@router.put("/update_transport/")
async def update_transport(transport_id: int, transport: TransportBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
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
    
@router.get("/get_transport_data_by_id/")
async def get_transport_data_by_id(transport_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    transport_details = db.query(tbl_transports).filter(tbl_transports.transport_id == transport_id).first()
    if transport_details is not None:
        return {"status":"200","msg":"done",'response':transport_details}
    else:
        raise HTTPException(status_code=404, detail="transpotation  not found")


# delete api code for  transpotation
@router.delete("/delete_transport/")
async def delete_transport(transport_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    transport_data = db.query(tbl_transports).filter(tbl_transports.transport_id == transport_id).first()
    if transport_data is not None:
        transport_id = transport_data.transport_id
        db.delete(transport_data)
        db.commit()
        return {"status":"200","msg":"done",'response':{"transport_id":transport_id}}
    else:
        raise HTTPException(status_code=404, detail="transport not found")
