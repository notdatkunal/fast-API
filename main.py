import regex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importing of account router
from router import accounts,institute
from router.classes_module import sections,subjects,classes
from router.student_module import student,parents
from router.transport_module import stops,transports
app =FastAPI()
#CORS Middleware
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
app.include_router(
   institute.router,
   prefix="/Institute",
   tags=['Institute'],
)
#------------------------------------------STUDENTS START ---------------------------------------------------------
app.include_router(
   student.router,
   prefix="/Students",
   tags=['Students'],
)
app.include_router(
   parents.router,
   prefix="/Parents",
   tags=['Parents'],
)
#------------------------------STUDENTS END ---------------------------------------------------------
# -----------------------------CLASS,SECTIONS AND SUBJECTS STRAT------------------------------------------
app.include_router(
   classes.router,
   prefix="/Classes",
   tags=['Classes'],
)
app.include_router(
   sections.router,
   prefix="/Sections",
   tags=['Sections'],
)
app.include_router(
   subjects.router,
   prefix="/Subjects",
   tags=['Subjects'],
)
# -----------------------------CLASS,SECTIONS AND SUBJECTS END------------------------------------------
app.include_router(
   transports.router,
   prefix="/Transport",
   tags=['Transport'],
)
app.include_router(
   stops.router,
   prefix="/Stops",
   tags=['Stops'],
)




