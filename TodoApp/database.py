from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'          # (Sqlite) This URL is used to create location of this Sqlite database on our FastAPI application
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234@localhost/TodoApplicationDatabase'          # (PostgreSQL) This URL is used to create location of this PostgreSQL database on our FastAPI application
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test1234@127.0.0.1:3306/TodoApplicationDatabase'          # (MySQL) This URL is used to create location of this MySQL database on our FastAPI application

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})            # (Sqlite) Create the database engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)                 # (PostgreSQL or MySQL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)            # Create a session factory

Base = declarative_base()                # Create a base class for our models to inherit from
