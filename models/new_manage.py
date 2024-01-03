from .students import Student,Parents
from .classes import Classes,Sections
from sqlalchemy.orm import joinedload,Load,load_only
from fastapi import HTTPException


from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

class StudentManager:
    def __init__(self, db):
        self.db = db

    def get_data_field(self, field_name, field_value):
        try:
            self.student_data = (
                self.db.query(Student)
                .join(Classes, Student.class_id == Classes.class_id)
                .join(Sections, Student.section_id == Sections.section_id)
                .options(joinedload(Student.classes).load_only(Classes.class_name))
                .options(joinedload(Student.sections).load_only(Sections.section_name))
                .filter(getattr(Student, field_name) == field_value, Student.is_deleted == False)
                .all()
            )
            return self.student_data
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

        