from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
import Enum
import models

# used to prevent cross origin ttacks
from fastapi.middleware.cors import CORSMiddleware


from database import SessionLocal, engine


app = FastAPI()

origins = ["http://localhost:3000"]

# prevents access cross origin attacks by only allowing requests from the react server port 3000 of localhost
app.add_middleware(CORSMiddleware, allow_origins=origins)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
