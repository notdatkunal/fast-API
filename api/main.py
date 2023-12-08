import regex
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importing of account router
from router import accounts,institute,students
app =FastAPI()
origins = ['http://127.0.0.1:8001','http://127.0.0.1:8002','http://127.0.0.1:8003','http://127.0.0.1:8004']

#CORS Middleware
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
app.include_router(
   accounts.router,
   prefix="/Accounts",
   tags=["Accounts"],
)
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




