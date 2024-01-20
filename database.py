
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://gurukulprodcimysqladmin:HyIa0MInqwdpD3N@gurukul-prod-ci-mysqlserver.mysql.database.azure.com:3306/gurukul-prod-ci-mysqldb"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"ssl_ca": "DigiCertGlobalRootCA.crt.pem"})

# Create a SessionLocal class to use for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
BASE: DeclarativeMeta = declarative_base()



