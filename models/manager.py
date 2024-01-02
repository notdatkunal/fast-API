from alchmanager import ManagedQuery, BaseQueryManager
# import all models
from models.students import Student,Parents
from models.assignments import Assignments
from models.classes import Classes,Sections
from models.classes import Classes
from models.staffs import Staff
from fastapi import HTTPException
from sqlalchemy.orm import joinedload,Load,load_only
from fastapi import status

# create modelmanager for all models
class ModelManager(BaseQueryManager):

    @staticmethod
    def get_data_by_field(query: ManagedQuery, field_name: str, field_value: str,model_name) -> ManagedQuery:
        try:
            data = query.filter(getattr(model_name, field_name) == field_value and model_name.is_deleted == False).all()
            return data
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    # -------student model manager----------------
    @staticmethod
    def get_student_data_by_institute(query: ManagedQuery,institite_id: int) -> ManagedQuery:
        try:
            data = query.filter(Student.institute_id == institite_id).all()
            # data = query.filter(Student.institute_id == institite_id).all()
            return data
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    # -------student model manager----------------
    # -------classes model manager----------------
    @staticmethod
    def get_classes_by_institute(query: ManagedQuery, institite_id: int) -> ManagedQuery:
        return query.filter(Classes.institute_id == institite_id and Classes.is_deleted == False)
    
    # -------classes model manager----------------

    # -------Staff model manager------------------
    @staticmethod
    def get_data_by_institute(query: ManagedQuery,model,institite_id: int) -> ManagedQuery:
        try:
            data = query.filter(model.institute_id == institite_id and model.is_deleted == False).all()
            return data
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def get_assignment_for_student_tab(class_id:int,section_id:int,db:ManagedQuery):
        try:
            assignment_data = (
                db.query(Assignments)
                .join(Classes, Assignments.class_id == Classes.class_id)
                .join(Sections, Assignments.section_id == Sections.section_id)
                .options(joinedload(Assignments.classes).load_only(Classes.class_name))
                .options(joinedload(Assignments.sections).load_only(Sections.section_name))
                .filter(Assignments.class_id == class_id and Assignments.section_id == section_id and Assignments.is_deleted == False)
                .all()
            )
            return assignment_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))