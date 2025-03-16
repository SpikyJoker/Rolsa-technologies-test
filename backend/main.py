from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Dict
import jwt
import datetime
import base64
import traceback  # Import for detailed error tracing


app = FastAPI()

print("Starting FastAPI application...")

origins = [
    "http://localhost:5173",  # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock MySQL connection (in production, use proper connection pooling)
db = {"users": {}, "pdfs": {}}
print(
    f"Database initialized with {len(db['users'])} users and {len(db['pdfs'])} pdf entries"
)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


class User(BaseModel):
    username: str
    password: str


class PDFData(BaseModel):
    filename: str
    content: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def pdf_to_base64(pdf_path: str) -> str:
    try:
        if isinstance(pdf_path, bytes):
            pdf_binary = pdf_path
        else:
            with open(pdf_path, "rb") as pdf_file:
                pdf_binary = pdf_file.read()
        base64_string = base64.b64encode(pdf_binary).decode("utf-8")
        return base64_string
    except Exception as e:
        print(f"Error in pdf_to_base64: {str(e)}")
        print(traceback.format_exc())
        return None


# Function to convert Base64 string back to PDF
def base64_to_pdf_binary(base64_string):
    print(
        f"Converting base64 string to PDF binary, string length: {len(base64_string)}"
    )
    try:
        # Decode Base64 string to binary data
        pdf_binary = base64.b64decode(base64_string)
        print(f"Base64 decoded to binary, size: {len(pdf_binary)} bytes")
        # Write binary data to a new PDF file
        return pdf_binary
    except Exception as e:
        print(f"Error in base64_to_pdf_binary: {str(e)}")
        print(traceback.format_exc())
        return None


def create_token(username: str):
    print(f"Creating token for user: {username}")
    to_encode = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"Token created successfully for {username}")
        return encoded_jwt
    except Exception as e:
        print(f"Error creating token: {str(e)}")
        print(traceback.format_exc())
        raise


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Authenticating token: {token[:10]}...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"Token decoded for user: {username}")

        if username not in db["users"]:
            print(f"Authentication failed: User {username} not found in database")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print(f"User {username} authenticated successfully")
        return username
    except jwt.ExpiredSignatureError:
        print("Authentication failed: Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        print("Authentication failed: Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/register")
async def register(user: User):
    print(f"Registration attempt for username: {user.username}")
    if user.username in db["users"]:
        print(f"Registration failed: Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already exists")

    db["users"][user.username] = {"password": user.password}
    print(f"User {user.username} registered successfully")
    return {"message": "User registered successfully"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for username: {form_data.username}")

    if form_data.username not in db["users"]:
        print(f"Login failed: Username {form_data.username} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if db["users"][form_data.username]["password"] != form_data.password:
        print(f"Login failed: Invalid password for {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(form_data.username)
    print(f"Login successful for {form_data.username}, token generated")
    return {"access_token": token, "token_type": "bearer"}


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...), current_user: str = Depends(get_current_user)
):
    print(f"PDF upload attempt by user {current_user}, filename: {file.filename}")

    if not file.filename.endswith(".pdf"):
        print(f"Upload rejected: File {file.filename} is not a PDF")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        content = await file.read()
        print(f"File read successful, size: {len(content)} bytes")

        text_content = pdf_to_base64(content)
        if text_content is None:
            print("PDF conversion to base64 failed")
            raise HTTPException(status_code=500, detail="Error processing PDF file")

        pdf_id = f"{current_user}_{len(db['pdfs'].get(current_user, {}))}"
        if current_user not in db["pdfs"]:
            db["pdfs"][current_user] = {}

        db["pdfs"][current_user][pdf_id] = {
            "filename": file.filename,
            "content": text_content,
        }
        print(f"PDF uploaded successfully with ID: {pdf_id}")
        return {"message": "PDF uploaded successfully", "pdf_id": pdf_id}
    except Exception as e:
        print(f"Error during PDF upload: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error uploading PDF: {str(e)}")


@app.get("/pdfs")
async def get_pdfs(current_user: str = Depends(get_current_user)):
    print(f"Fetching PDFs for user: {current_user}")
    # return "pdf"
    try:
        if current_user not in db["pdfs"]:
            print(f"No PDFs found for user {current_user}")
            return []

        user_pdfs = db["pdfs"].get(current_user, {})
        pdf_list = [
            {"pdf_id": pdf_id, "filename": data["filename"]}
            for pdf_id, data in user_pdfs.items()
        ]
        print(f"Found {len(pdf_list)} PDFs for user {current_user}")
        return pdf_list
    except Exception as e:
        print(f"Error fetching PDFs: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching PDFs: {str(e)}")


@app.get("/pdf/{pdf_id}")
async def get_pdf(pdf_id: str, current_user: str = Depends(get_current_user)):
    print(f"Retrieving PDF {pdf_id} for user {current_user}")

    try:
        if current_user not in db["pdfs"]:
            print(f"User {current_user} has no PDFs")
            raise HTTPException(status_code=404, detail="PDF not found")

        if pdf_id not in db["pdfs"][current_user]:
            print(f"PDF {pdf_id} not found for user {current_user}")
            raise HTTPException(status_code=404, detail="PDF not found")

        pdf_data = db["pdfs"][current_user][pdf_id]
        print(f"PDF {pdf_id} retrieved successfully")
        return pdf_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving PDF: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")


if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
