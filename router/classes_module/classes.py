import sys
sys.path.append("..")
from router.basic_import import *
from models.classes import Classes,Sections
from .sections import SectionBase
from router.utility import succes_response
# from .sections import 
import uuid

router = APIRouter()
# base models
class ClassBase(BaseModel):
    class_name : str = Field(min_length=3)
    is_deleted: bool = Field(default=False)
    institute_id:int

def generate_slug(class_name,db):
    slug = class_name.replace(" ", "-")
    while True:
        if db.query(Classes).filter(Classes.slug == slug).first():
            slug = slug + "-" + str(uuid.uuid4())[:4]
        else:
            return slug


@router.post("/create_class/")
async def create_class(class_data: ClassBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        class_instance = Classes(**class_data.dict())
        class_instance.slug = generate_slug(class_instance.class_name,db)
        db.add(class_instance)
        db.commit()
        db.refresh(class_instance)
        return succes_response(class_instance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

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
    
