import regex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importing of account router
from router import accounts,institute,students,classes,transport
app =FastAPI()
#CORS Middleware
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
# app.include_router(
#    accounts.router,
#    prefix="/Accounts",
#    tags=["Accounts"],
# )
app.include_router(
   institute.router,
   prefix="/Institute",
   tags=['Institute'],
)
app.include_router(
   students.router,
   prefix="/Students",
   tags=['Students'],
)
app.include_router(
   classes.router,
   prefix="/Classes",
   tags=['Classes'],
)
app.include_router(
   transport.router,
   prefix="/Transport",
   tags=['Transport'],
)




