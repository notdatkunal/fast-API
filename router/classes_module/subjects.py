import sys

sys.path.append("..")
from router.basic_import import *
from models.classes import Classes, Sections, Subjects
from router.utility import succes_response

router = APIRouter()


#  base model
class SubjectBase(BaseModel):
    subject_name: str = Field(min_length=3)
    class_id: int
    is_deleted: bool = Field(default=False)


@router.post("/create_subject/")
async def create_subject_for_class(
    subject_data: SubjectBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)
):
    # if (
    #     db.query(Subjects)
    #     .filter(
    #         Subjects.class_id == subject_data.class_id
    #         and Subjects.subject_name == subject_data.subject_name
    #     )
    #     .first()
    # ):
    #     raise HTTPException(status_code=400, detail="Subject already registered")
    try:
        subject_instance = Subjects(**subject_data.dict())
        db.add(subject_instance)
        db.commit()
        db.refresh(subject_instance)
        payload = succes_response(subject_instance)
        return payload
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")


@router.get("/get_all_sujects/")
async def get_all_sujects(db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    subject_obj = db.query(Subjects).filter(Subjects.is_deleted == False).all()
    return jsonable_encoder(subject_obj)


@router.get("/subject_id/")
async def get_subject_byId(subject_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    subject_data = (
        db.query(Subjects)
        .filter(Subjects.subject_id == subject_id, Subjects.is_deleted == False)
        .first()
    )
    if subject_data is not None:
        return {"status": "200", "msg": "done", "response": subject_data}
    else:
        raise HTTPException(status_code=404, detail="Subject not found")


@router.get("/get_subjects_by_class/")
async def get_subjects_by_class(class_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    class_instance = (
        db.query(Classes)
        .filter(Classes.class_id == class_id and Classes.is_deleted == False)
        .first()
    )
    if class_instance:
        subjects = (
            db.query(Subjects)
            .filter(Subjects.class_id == class_id, Subjects.is_deleted == False)
            .all()
        )
        return jsonable_encoder(subjects)
    else:
        return HTTPException(status_code=404, detail="Class not found")


@router.put("/update_subject_id/{subject_id}")
async def update_subject(
    subject_id: int, subjects: SubjectBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)
):
    subject_data = db.query(Subjects).filter(Subjects.subject_id == subject_id).first()
    if subject_id is not None:
        for key, value in subjects.dict(exclude_unset=True).items():
            setattr(subject_data, key, value)
        db.commit()
        db.refresh(subject_data)
        return {"status": "200", "msg": "done", "response": subject_data}
    else:
        raise HTTPException(status_code=404, detail="Subject not found")


@router.delete("/delete_subject_id/{subject_id}")
async def delete_subject(subject_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    subjects_data = db.query(Subjects).filter(Subjects.subject_id == subject_id).first()

    if subjects_data is not None:
        subjects_data.is_deleted = True
        db.commit()
        db.refresh(subjects_data)
        return {"status": "200", "msg": "done", "response": {"subject_id": subject_id}}
    else:
        raise HTTPException(status_code=404, detail="Subject not found")
