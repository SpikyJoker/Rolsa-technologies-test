from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict
import jwt
import datetime
import mysql.connector
from pdf2txt import convert_pdf_to_txt
import base64

app = FastAPI()

# Mock MySQL connection (in production, use proper connection pooling)
db = {"users": {}, "pdfs": {}}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


class User(BaseModel):
    username: str
    password: str


class PDFData(BaseModel):
    filename: str
    content: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str):
    to_encode = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username not in db["users"]:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/register")
async def register(user: User):
    print(user)
    if user.username in db["users"]:
        raise HTTPException(status_code=400, detail="Username already exists")
    db["users"][user.username] = {"password": user.password}
    return {"message": "User registered successfully"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username not in db["users"]
        or db["users"][form_data.username]["password"] != form_data.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...), current_user: str = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()
    text_content = convert_pdf_to_txt(content)

    pdf_id = f"{current_user}_{len(db['pdfs'].get(current_user, {}))}"
    if current_user not in db["pdfs"]:
        db["pdfs"][current_user] = {}

    db["pdfs"][current_user][pdf_id] = {
        "filename": file.filename,
        "content": text_content,
    }
    return {"message": "PDF uploaded successfully", "pdf_id": pdf_id}


@app.get("/pdfs")
async def get_pdfs(current_user: str = Depends(get_current_user)):
    user_pdfs = db["pdfs"].get(current_user, {})
    return [
        {"pdf_id": pdf_id, "filename": data["filename"]}
        for pdf_id, data in user_pdfs.items()
    ]


@app.get("/pdf/{pdf_id}")
async def get_pdf(pdf_id: str, current_user: str = Depends(get_current_user)):
    if current_user not in db["pdfs"] or pdf_id not in db["pdfs"][current_user]:
        raise HTTPException(status_code=404, detail="PDF not found")

    pdf_data = db["pdfs"][current_user][pdf_id]
    return pdf_data


"""
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

"""
