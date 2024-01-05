from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.staffs import Staff,StaffDocuments
from router.utility import succes_response

router = APIRouter()

# base model
class StaffDocumentsBase(BaseModel):
    document_name: Optional[str]
    document_file: Optional[str]
    staff_id: int
    is_deleted :bool = False


@router.post("/add_staff_documents/")
async def create_staff_documents(staff_documents:StaffDocumentsBase, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    if db.query(Staff).filter(Staff.staff_id == staff_documents.staff_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    try:
        new_staff_documents = StaffDocuments(**staff_documents.dict())
        db.add(new_staff_documents)
        db.commit()
        db.refresh(new_staff_documents)
        return succes_response(new_staff_documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/get_staff_documents_by_staff_id/")
async def get_staff_documents(staff_id:int, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    if db.query(Staff).filter(Staff.staff_id == staff_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    staff_documents = db.query(StaffDocuments).filter(StaffDocuments.staff_id == staff_id).all()
    if staff_documents is not None:
        return succes_response(staff_documents)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff Documents not found")

@router.get("/get_staff_documents_by_id/")
async def get_staff_documents_by_id(document_id:int, db:Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    staff_document = db.query(StaffDocuments).filter(StaffDocuments.document_id == document_id).first()
    if staff_document is not None:
        return succes_response(staff_document)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff Documents not found")
    
@router.put("/update_staff_documents/")
async def update_staff_documents(document_id: int, staff_documents: StaffDocumentsBase, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    if db.query(Staff).filter(Staff.staff_id == staff_documents.staff_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    staff_document = db.query(StaffDocuments).filter(StaffDocuments.document_id == document_id).first()
    if staff_document is not None:
        try:
            for key, value in staff_documents.dict(exclude_unset=True).items(): 
                setattr(staff_document, key, value)
            db.commit()
            db.refresh(staff_document)
            return succes_response(staff_document)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error While Updating: {str(e)}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff Documents not found")
    

@router.delete("/delete_staff_documents/")
async def delete_staff_documents(document_id: int, db: Session = Depends(get_db),current_user: str = Depends(is_authenticated)):
    staff_document = db.query(StaffDocuments).filter(StaffDocuments.document_id == document_id).first()
    if staff_document is not None:
        db.delete(staff_document)
        db.commit()
        return succes_response("Staff Documents Deleted Successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff Documents not found")