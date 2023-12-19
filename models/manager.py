from alchmanager import ManagedQuery, BaseQueryManager
# import all models
from models.students import Student,Parents
from models.classes import Classes
from models.staffs import Staff
from fastapi import HTTPException
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
    def get_student_data_by_institute(query: ManagedQuery, institute_id: int) -> ManagedQuery:
        try:
            data = query.filter(Student.institute_id == institute_id).all()
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
        