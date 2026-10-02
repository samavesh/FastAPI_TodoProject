import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})            # (Sqlite) Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)                 # (PostgreSQL or MySQL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)            # Create a session factory

Base = declarative_base()                # Create a base class for our models to inherit from
