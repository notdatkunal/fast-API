import sys

sys.path.append("..")
from router.basic_import import *
from models.classes import Classes, Sections
from router.utility import succes_response

router = APIRouter()


# base models
class SectionBase(BaseModel):
    section_name: str = Field(min_length=3)
    is_deleted: bool = Field(default=False)
    class_id: int


# post method for Section
@router.post("/create_section/",)
async def create_section_for_class(
    section_data: SectionBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    try:
        section_instance = Sections(**section_data.dict())
        db.add(section_instance)
        db.commit()
        db.refresh(section_instance)
        payload = succes_response(section_instance)
        return payload
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")


@router.get("/get_all_sections/")
async def get_all_sections(db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    section_obj = db.query(Sections).filter(Sections.is_deleted == False).all()
    return jsonable_encoder(section_obj)


@router.get("/section_id/")
async def get_section_byId(section_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    section_data = (
        db.query(Sections)
        .filter(Sections.section_id == section_id, Sections.is_deleted == False)
        .first()
    )

    if section_data is not None:
        return {"status": "200", "msg": "done", "response": section_data}

    else:
        raise HTTPException(status_code=404, detail="Section not found")


@router.get("/get_sections_by_class/")
async def get_sections_by_class(class_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    class_instance = (
        db.query(Classes)
        .filter(Classes.class_id == class_id, Classes.is_deleted == False)
        .first()
    )
    if class_instance:
        sections = (
            db.query(Sections)
            .filter(Sections.class_id == class_id, Sections.is_deleted == False)
            .all()
        )
        return jsonable_encoder(sections)
    else:
        return HTTPException(status_code=404, detail="Class not found")


@router.put("/update_section_id/{section_id}")
async def update_section(
    section_id: int, sections: SectionBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)
):
    section_data = db.query(Sections).filter(Sections.section_id == section_id).first()
    if section_data is not None:
        for key, value in sections.dict(exclude_unset=True).items():
            setattr(section_data, key, value)
        db.commit()
        db.refresh(section_data)
        return {"status": "200", "msg": "done", "response": section_data}
    else:
        raise HTTPException(status_code=404, detail="Section not found")


@router.delete("/delete_section_id/{section_id}")
async def delete_section(section_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    section_data = db.query(Sections).filter(Sections.section_id == section_id).first()

    if section_data is not None:
        section_data.is_deleted = True
        db.commit()
        db.refresh(section_data)
        return {"status": "200", "msg": "done", "response": {"section_id": section_id}}
    else:
        raise HTTPException(status_code=404, detail="Section not found")
