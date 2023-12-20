from sqlalchemy import create_engine,pool
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql://a6e9a1_gsmpoc:gsmpoc@2023@MYSQL5044.site4now.net:3306/db_a6e9a1_gsmpoc"
SQLALCHEMY_DATABASE_URL = "mysql://a6e9a1_gsmpoc:gsmpoc2023@MYSQL5044.site4now.net:3306/db_a6e9a1_gsmpoc"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.QueuePool, pool_size=20, max_overflow=40)

# Create a SessionLocal class to use for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
BASE: DeclarativeMeta = declarative_base()

