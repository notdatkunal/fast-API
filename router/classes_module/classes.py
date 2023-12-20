import sys
sys.path.append("..")
from router.basic_import import *
from models.classes import Classes,Sections
from .sections import SectionBase
from router.utility import succes_response
# from .sections import 

router = APIRouter()
# base models
class ClassBase(BaseModel):
    class_name : str = Field(min_length=3)
    slug:str
    is_deleted: bool = Field(default=False)
    institute_id:int


@router.post("/create_class/")
async def create_class(class_data: ClassBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        class_instance = Classes(**class_data.dict())
        db.add(class_instance)
        db.commit()
        db.refresh(class_instance)
        payload = class_instance

        section_data = {
            "section_name": "Section A",
            'class_id': class_instance.class_id,
            "is_deleted": False
        }
        section_instance =Sections(**section_data)
        db.add(section_instance)
        db.commit()
        return succes_response(payload)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/get_classes_by_institute/")
async def get_all_classes(institite_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    classes_obj =ModelManager.get_classes_by_institute(db.query(Classes),institite_id).filter(Classes.is_deleted == False).all()
    return jsonable_encoder(classes_obj)


@router.get("/class_id/")
async def get_class_by_classId(class_id:int,db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    classes_data=db.query(Classes).filter(Classes.class_id == class_id,Classes.is_deleted == False).first()
    if classes_data is not None:
        return {"status":"200","msg":"done",'response':classes_data}
    else:
        raise HTTPException(status_code=404, detail="Class not found")
    

@router.get("/get_classes_by_field/{field_name}/{field_value}/")
async def get_all_classes_by_field(field_name:str,field_value:str,db:Session = Depends(get_db)):
    class_model = Classes
    classes_obj =ModelManager.get_data_by_field(db.query(class_model),field_name,field_value,class_model)
    return jsonable_encoder(classes_obj)





@router.put("/{class_id}")
async def update_class(class_id: int, classes: ClassBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)) :
    classes_data=db.query(Classes).filter(Classes.class_id == class_id).first()
    if classes_data is not None:
        for key ,value in classes.dict(exclude_unset=True).items():
            setattr(classes_data, key ,value)
        db.commit()
        db.refresh(classes_data)    
        return {"status":"200","msg":"done",'response':classes_data}
    else:
        raise HTTPException(status_code=404, detail="Class not found")             

@router.delete("/{class_id}")
async def delete_class(class_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    classes_data = db.query(Classes).filter(Classes.class_id == class_id).first()
    
    if classes_data is not None:
        classes_data.is_deleted = True
        db.commit()
        db.refresh(classes_data)
        return {"status": "200", "msg": "done", 'response': {'class_id': class_id}}
    else:
        raise HTTPException(status_code=404, detail="Class not found")
    
