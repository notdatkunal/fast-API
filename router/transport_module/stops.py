from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.transports import Stops 
from router.utility import succes_response

router = APIRouter()

# base schema
class StopsBase(BaseModel):
    stop_name : str = Field(min_length=3)
    transport_id : int

@router.post("/create_stopage/")
async def create_stopage(stopage_data:StopsBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        stopage_instnace = Stops(**stopage_data.dict())
        db.add(stopage_instnace)
        db.commit()
        db.refresh(stopage_instnace)
        return succes_response(stopage_instnace,msg="Stopage Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")


@router.get("/get_all_stopages/")
async def get_all_stopages(db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    return jsonable_encoder(db.query(Stops).all())

# code for all stopages by transport id
@router.get("/get_all_stopages_by_transport/")
async def get_all_stopages(transport_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    data = db.query(Stops).filter(Stops.transport_id==transport_id).all()
    if data is not None:
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=404,detail="stopage not found")

# code for update stopage
@router.put("/update_stop/")
async def update_stop(stop_id:int,stop:StopsBase,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    stop_data = db.query(Stops).filter(Stops.stop_id==stop_id).first()
    if stop_data is not None:
        for key,value in stop.dict(exclude_unset=True).items():
            setattr(stop_data,key,value)
        db.commit()
        db.refresh(stop_data)
        return succes_response(stop_data,msg="Stopage Updated Successfully")
    else:
        raise HTTPException(status_code=404,detail="stopage not found")

# code for delete stopage
@router.delete("/delete_stop/")
async def delete_stop(stop_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    stop_data = db.query(Stops).filter(Stops.stop_id==stop_id).first()
    if stop_data is not None:
        db.delete(stop_data)
        db.commit()
        return succes_response("",msg="Stopage Deleted Successfully")
    else:
        raise HTTPException(status_code=404,detail="stopage not found")