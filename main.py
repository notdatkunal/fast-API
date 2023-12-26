import regex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importing of account router
from router import accounts,institute
from router.classes_module import sections,subjects,classes
from router.student_module import student,parents
from router.transport_module import stops,transports
from router.staffs_module import staff,staff_payrole
from router.users import user,login
from router.notice_module import notice
from router.assignments import assignment
from router.calender import calender
from router.users.login import *
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
# app.include_router(
#    accounts.router,
#    prefix="/Accounts",
#    tags=['Accounts'],
# )
# ------------------------------------------ACCOUNTS END ---------------------------------------------------------
# ------------------------------------------Assignment ---------------------------------------------------------
app.include_router(
   assignment.router,
   prefix="/Assignments",
   tags=['Assignments'],
)
# ------------------------------------------Assignment ---------------------------------------------------------
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
# ------------------------------------------Classes ---------------------------------------------------------
# ------------------------------------------Notices ---------------------------------------------------------
app.include_router(
   notice.router,
   prefix="/Notice",
   tags=['Notice'],
)
# ------------------------------------------Notices ---------------------------------------------------------
# ------------------------------------------Parents ---------------------------------------------------------
app.include_router(
   parents.router,
   prefix="/Parents",
   tags=['Parents'],
)
# ------------------------------------------Parents ---------------------------------------------------------
# ------------------------------------------Sections ---------------------------------------------------------
app.include_router(
   sections.router,
   prefix="/Sections",
   tags=['Sections'],
)
# ------------------------------------------Sections ---------------------------------------------------------
# ------------------------------------------Staff ---------------------------------------------------------
app.include_router(
   staff.router,
   prefix="/Staff",
   tags=['Staff'],
)
# ------------------------------------------Staff ---------------------------------------------------------
# ------------------------------------------Staff Payrole ---------------------------------------------------------
app.include_router(
   staff_payrole.router,
   prefix="/StaffPayrole",
   tags=['StaffPayrole'],
)
# ------------------------------------------Staff Payrole ---------------------------------------------------------
# ------------------------------------------Stops ---------------------------------------------------------
app.include_router(
   stops.router,
   prefix="/Stops",
   tags=['Stops'],
)
# ------------------------------------------Stops ---------------------------------------------------------
# ------------------------------------------Students ---------------------------------------------------------
app.include_router(
   student.router,
   prefix="/Students",
   tags=['Students'],
)
# ------------------------------------------Students ---------------------------------------------------------
# ------------------------------------------Subjects ---------------------------------------------------------
app.include_router(
   subjects.router,
   prefix="/Subjects",
   tags=['Subjects'],
)
# ------------------------------------------Subjects ---------------------------------------------------------
# ------------------------------------------Transports ---------------------------------------------------------
app.include_router(
   transports.router,
   prefix="/Transports",
   tags=['Transports'],
)
# ------------------------------------------Transports ---------------------------------------------------------
# ------------------------------------------Users ---------------------------------------------------------
app.include_router(
   user.router,
   prefix="/Users",
   tags=['Users'],
)
# ------------------------------------------Users ---------------------------------------------------------

