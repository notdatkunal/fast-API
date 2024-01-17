from database import BASE
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float
import sys

sys.path.append("..")
from pydantic import validator
from router.basic_import import *
from models.classes import Classes
from models.examination import ParentExam, Exam
from models.grade import Grades, grades_classes_association
from models.students import Student
from router.utility import succes_response

router = APIRouter()


class MarkEntry(BaseModel):
    student_id: int
    subject: str
    marks: float


class ExcelData(BaseModel):
    entries: List[MarkEntry]


# @router.post("/upload_excel/")
# async def upload_excel(
#     excel_file: UploadFile = File(...),
#     additional_data: str = Form(...),
# ):
#     try:
#         # Process the Excel file and additional data
#         data = await process_excel_data(excel_file.file, additional_data)
#         return JSONResponse(content={"message": "Data processed successfully", "data": data})
#     except Exception as e:
#         return JSONResponse(content={"message": "Error processing data", "error": str(e)}, status_code=500)


from sqlalchemy.exc import SQLAlchemyError


def get_parent_exam(db, parent_exam_id):
    try:
        parent_exam = (
            db.query(ParentExam)
            .filter(ParentExam.parent_exam_id == parent_exam_id)
            .first()
        )
        if parent_exam is None or parent_exam.is_deleted:
            raise HTTPException(status_code=404, detail="Parent Exam not found")
        return parent_exam
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing the database: {str(e)}"
        )


def get_student_data(db, student_id):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def get_exams(db, parent_exam_id):
    try:
        exams = db.query(Exam).filter(Exam.parent_exam_id == parent_exam_id).all()
        if not exams:
            raise HTTPException(status_code=404, detail="Exams not found")
        return exams
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing the database: {str(e)}"
        )


def get_grade(percentage, class_id, db):
    grade = (
        db.query(Grades)
        .join(
            grades_classes_association,
            Grades.grade_id == grades_classes_association.c.grade_id,
        )
        .filter(
            grades_classes_association.c.class_id == class_id,
            Grades.percent_from <= percentage,
            Grades.percent_upto >= percentage,
        )
        .options(joinedload(Grades.grades))
        .first()
    )
    if grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade.grade_name


def create_result_table(parent_exam_id, db):
    parent_exam = get_parent_exam(db, parent_exam_id)
    exams = get_exams(db, parent_exam_id)

    result_table_name = f"tbl_{parent_exam.parent_exam_slug}_result"

    columns = [
        Column("result_id", Integer, primary_key=True, autoincrement=True),
        Column(
            "student_id",
            Integer,
            ForeignKey("tbl_students.student_id", ondelete="SET NULL"),
        ),
        Column("institute_id", Integer, ForeignKey("institute.id", ondelete="CASCADE")),
        Column(
            "parent_exam_id",
            Integer,
            ForeignKey("tbl_parent_exams.parent_exam_id", ondelete="SET NULL"),
        ),
        Column("is_deleted", Boolean, default=False),
        Column("total_marks", Float),
        Column("percentage", Float),
        Column("grade", String(255)),
        Column("result_status", Boolean, default=False),
    ]

    for exam in exams:
        subject_slug = exam.subject.subject_name.lower().replace(" ", "_")
        column_grade = Column(f"{subject_slug}_grade", String(255))
        columns.append(Column(subject_slug, Float))
        columns.append(column_grade)

    try:
        result_table = Table(result_table_name, BASE.metadata, *columns)
        return result_table
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating result table: {str(e)}"
        )


@router.get("/create_result_table/")
async def create_result_table_api(parent_exam_id: int, db: db_dependency):
    result_table = create_result_table(parent_exam_id, db)
    result_table.create(db.bind)
    return succes_response(
        data=result_table.name, msg="Result table created successfully"
    )


@router.post("/store_result/")
async def store_result(
    parent_exam_id: int, student_id: int, db: db_dependency, data: dict = {}
):
    parent_exam = get_parent_exam(db, parent_exam_id)
    student = get_student_data(db, student_id)
    exams_data = get_exams(db, parent_exam_id)
    grade = get_grade((sum(data.values()) / 75), student.class_id, db)
    result_table_name = (
        f"tbl_{parent_exam.parent_exam_slug}_result"  # get result table name
    )
    result_table = Table(
        result_table_name, BASE.metadata, autoload_with=db.bind
    )  # get result table
    # check if result already stored
    if (
        db.query(result_table).filter(result_table.c.student_id == student_id).first()
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Result already stored"
        )
    basic_data = {
        "institute_id": parent_exam.institute_id,
        "parent_exam_id": parent_exam.parent_exam_id,
        "student_id": student.student_id,
        "is_deleted": False,
        "result_status": True,
    }
    try:
        basic_data.update(data)
        for exam in exams_data:
            subject_slug = exam.subject.subject_name.lower().replace(" ", "_")
            subject_grade = get_grade(data[subject_slug]/exam.full_marks,student.class_id, db)
            basic_data.update({f"{subject_slug}_grade":subject_grade})
        basic_data.update({"total_marks": sum(data.values())})
        basic_data.update({"percentage": (sum(data.values()) / len(data.values()))})
        db.execute(result_table.insert().values(**basic_data))
        db.commit()
        return succes_response(data="", msg="Result stored successfully")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error storing result: {str(e)}")


@router.get("/get_all_result_by_parent_exam_id/")
async def get_all_result_by_parent_exam_id(parent_exam_id: int, db: db_dependency):
    parent_exam = get_parent_exam(db, parent_exam_id)
    result_table_name = f"tbl_{parent_exam.parent_exam_slug}_result"
    result_table = Table(result_table_name, BASE.metadata, autoload_with=db.bind)
    try:
        result = db.execute(result_table.select()).mappings().all()
        return succes_response(data=result, msg="Result fetched successfully")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching result: {str(e)}")


@router.get("/get_result_by_student_id/")
async def get_result_by_student_id(
    parent_exam_id: int, student_id: int, db: db_dependency
):
    student = get_student_data(db, student_id)
    parent_exam = get_parent_exam(db, parent_exam_id)
    result_table_name = f"tbl_{parent_exam.parent_exam_slug}_result"
    result_table = Table(result_table_name, BASE.metadata, autoload_with=db.bind)
    try:
        result = db.execute(
            result_table.select().where(result_table.c.student_id == student.student_id)
        ).first()
        return succes_response(data=result, msg="Result fetched successfully")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching result: {str(e)}")
