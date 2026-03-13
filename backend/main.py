from gemini_service import generate_questions
from fastapi import FastAPI
from pydantic import BaseModel
from database import users

from typing import Optional
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    name: Optional[str] = None
    email: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/signup")
def signup(user: User):
    existing_user = users.find_one({"email": user.email})
    if existing_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    users.insert_one(user_dict)
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: User):
    existing_user = users.find_one({"email": user.email})
    
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {"message": "Login successful"}

from fastapi import UploadFile
@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    return {"message": "Resume uploaded successfully"}

@app.post("/generate-questions")
def get_questions(data: dict):

    skills = data["skills"]

    questions = generate_questions(skills)

    return {"questions": questions}

from database import interviews

@app.post("/save-result")
def save_result(data: dict):

    interviews.insert_one({
        "user": data["user"],
        "questions": data["questions"],
        "answers": data["answers"],
        "confidence": data["confidence"],
        "score": data["score"]
    })

    return {"message": "Result saved"}