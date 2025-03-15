from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = ""

engine = create_engine(
    URL_DATABASE, connect_args={"check_same_thread": False}
)  # Creates a SQLAlchemy engine that will interact with the database

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Creates a configured "Session" that is bound to the engine

Base = (
    declarative_base()
)  # This defines the base class which the mapped classes will inherit from
