from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from models.students import Student,StudentsDocuments
from router.utility import succes_response

router = APIRouter()

# base model
class StudentDocumentsBase(BaseModel):
    document_name: Optional[str]
    document_file: Optional[str]
    student_id: int
    is_deleted :bool = False


@router.post("/add_student_documents/")
async def create_student_documents(student_documents: StudentDocumentsBase, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    if db.query(Student).filter(Student.student_id == student_documents.student_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    try:
        new_student_documents = StudentsDocuments(**student_documents.dict())
        db.add(new_student_documents)
        db.commit()
        db.refresh(new_student_documents)
        return succes_response(new_student_documents,msg="Student Documents Created Successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error While Creating: {str(e)}")

@router.get("/get_student_documents_by_student_id/")
async def get_student_documents(student_id: int, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    if db.query(Student).filter(Student.student_id == student_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student_documents = db.query(StudentsDocuments).filter(StudentsDocuments.student_id == student_id).all()
    if student_documents is not None:
        return succes_response(student_documents)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Documents not found")

@router.get("/get_student_documents_by_id/")
async def get_student_documents_by_id(document_id: int, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    student_document = db.query(StudentsDocuments).filter(StudentsDocuments.document_id == document_id).first()
    if student_document is not None:
        return succes_response(student_document)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Documents not found")
    
@router.put("/update_student_documents/")
async def update_student_documents(document_id: int, student_documents: StudentDocumentsBase, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    if db.query(Student).filter(Student.student_id == student_documents.student_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    student_document = db.query(StudentsDocuments).filter(StudentsDocuments.document_id == document_id).first()
    if student_document is not None:
        try:
            for key, value in student_documents.dict(exclude_unset=True).items(): 
                setattr(student_document, key, value)
            db.commit()
            db.refresh(student_document)
            return succes_response(student_document,msg="Student Documents Updated Successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error While Updating: {str(e)}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Documents not found")
    

@router.delete("/delete_student_documents/")
async def delete_student_documents(document_id: int, db: Session = Depends(get_db), current_user: str = Depends(is_authenticated)):
    student_document = db.query(StudentsDocuments).filter(StudentsDocuments.document_id == document_id).first()
    if student_document is not None:
        db.delete(student_document)
        db.commit()
        return succes_response("",msg='Student Documents Deleted Successfully')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Documents not found")
