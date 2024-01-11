from datetime import date
import sys
sys.path.append("..")
from router.basic_import import *
from router.utility import succes_response
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager