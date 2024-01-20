import regex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import institute
from router.account_module import accounts
from router.classes_module import sections,subjects,classes
from router.student_module import student,parents,students_documents
from router.transport_module import stops,transports
from router.staffs_module import staff,staff_payrole,staff_documents
from router.users import user,login
from router.notice_module import notice
from router.assignments import assignment,assignment_sunmission
from router.calender import calender
from router.grade import grade
from router.attendance import student_attendance,staff_attendance
from router.exams import parent_exam,exam,result
from router.fee_module import fees,student_fee
from router.activity_module import activity
from router.education_year import education
from router.users.login import *
from router import azure_blobs
app = FastAPI(
   title="GSM API",
   description="GURUKUL A School Management System",
   version="1.0.0",
)
#CORS Middleware
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"], 
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
#We not using blob 
app.include_router(
   result.router,
   prefix="/Result",
   tags=['Result'],
)

#------------------------------------------Azure Blobs START ---------------------------------------------------------
app.include_router(
   azure_blobs.router,
   prefix="/AzureBlobs",
   tags=['AzureBlobs'],
)
#------------------------------------------LOGIN START ---------------------------------------------------------
app.include_router(
   login.router,
   prefix="/Login",
   tags=['Login'],
)
#------------------------------------------LOGIN END ---------------------------------------------------------
app.include_router(
   institute.router,
   prefix="/Institute",
   tags=['Institute'],
)
# ------------------------------------------ACCOUNTS START ---------------------------------------------------------
app.include_router(
   accounts.router,
   prefix="/Accounts",
   tags=['Accounts'],
)
# ------------------------------------------Activity ---------------------------------------------------------
app.include_router(
   activity.router,
   prefix="/Activity",
   tags=['Activity'],
)
# ------------------------------------------Assignment ---------------------------------------------------------
app.include_router(
   assignment.router,
   prefix="/Assignments",
   tags=['Assignments'],
)
# ------------------------------------------Assignment Submission ---------------------------------------------------------
app.include_router(
   assignment_sunmission.router,
   prefix="/AssignmentSubmission",
   tags=['AssignmentSubmission'],
)
# ------------------------------------------Calender ---------------------------------------------------------
app.include_router(
   calender.router,
   prefix="/Calender",
   tags=['Calender'],
)
# ------------------------------------------Calender ---------------------------------------------------------
# ------------------------------------------Classes ---------------------------------------------------------
app.include_router(
   classes.router,
   prefix="/Classes",
   tags=['Classes'],
)
# ------------------------------------------Education ---------------------------------------------------------
app.include_router(
   education.router,
   prefix="/EducationYear",
   tags=['EducationYear'],
)
# ------------------------------------------Exams ---------------------------------------------------------
app.include_router(
   exam.router,
   prefix="/Exams",
   tags=['Exams'],
)
# ------------------------------------------Fees ---------------------------------------------------------
app.include_router(
   fees.router,
   prefix="/Fees",
   tags=['Fees'],
)
# ------------------------------------------Grades ---------------------------------------------------------
app.include_router(
   grade.router,
   prefix="/Grades",
   tags=['Grades'],
)
# ------------------------------------------Notices ---------------------------------------------------------
app.include_router(
   notice.router,
   prefix="/Notice",
   tags=['Notice'],
)
# ------------------------------------------Parents ---------------------------------------------------------
app.include_router(
   parents.router,
   prefix="/Parents",
   tags=['Parents'],
)
# ------------------------------------------Exams ---------------------------------------------------------
app.include_router(
   parent_exam.router,
   prefix="/ParentExams",
   tags=['ParentExams'],
)
# ------------------------------------------Sections ---------------------------------------------------------
app.include_router(
   sections.router,
   prefix="/Sections",
   tags=['Sections'],
)
# ------------------------------------------Staff ---------------------------------------------------------
app.include_router(
   staff.router,
   prefix="/Staff",
   tags=['Staff'],
)
# ------------------------------------------Staff Attendance ---------------------------------------------------------
app.include_router(
   staff_attendance.router,
   prefix="/StaffAttendance",
   tags=['StaffAttendance'],
)
# ------------------------------------------Staff Documents ---------------------------------------------------------
app.include_router(
   staff_documents.router,
   prefix="/StaffDocuments",
   tags=['StaffDocuments'],
)
# ------------------------------------------Staff Payrole ---------------------------------------------------------
app.include_router(
   staff_payrole.router,
   prefix="/StaffPayrole",
   tags=['StaffPayrole'],
)
# ------------------------------------------Stops ---------------------------------------------------------
app.include_router(
   stops.router,
   prefix="/Stops",
   tags=['Stops'],
)
# ------------------------------------------Students ---------------------------------------------------------
app.include_router(
   student.router,
   prefix="/Students",
   tags=['Students'],
)
# ------------------------------------------Student Attendance ---------------------------------------------------------
app.include_router(
   student_attendance.router,
   prefix="/StudentAttendance",
   tags=['StudentAttendance'],
)
# ------------------------------------------Students Documents ---------------------------------------------------------
app.include_router(
   students_documents.router,
   prefix="/StudentsDocuments",
   tags=['StudentsDocuments'],
)
# ------------------------------------------Student Fee ---------------------------------------------------------
app.include_router(
   student_fee.router,
   prefix="/StudentFee",
   tags=['StudentFee'],
)
# ------------------------------------------Subjects ---------------------------------------------------------
app.include_router(
   subjects.router,
   prefix="/Subjects",
   tags=['Subjects'],
)
# ------------------------------------------Transports ---------------------------------------------------------
app.include_router(
   transports.router,
   prefix="/Transports",
   tags=['Transports'],
)
# ------------------------------------------Users ---------------------------------------------------------
app.include_router(
   user.router,
   prefix="/Users",
   tags=['Users'],
)

