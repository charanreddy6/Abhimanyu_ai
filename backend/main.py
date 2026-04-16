from gemini_service import generate_questions, suggest_skills_and_roles, evaluate_answers
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
from pydantic import BaseModel
from database import users

from typing import Optional
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional, List
import bcrypt

class User(BaseModel):
    name: Optional[str] = None
    email: str
    password: str

class EvaluationRequest(BaseModel):
    questions: List[str]
    answers: List[str]
    role: str
    skills: List[str]

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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
from resume_parser import extract_skills

@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    
    file_path = file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    skills = extract_skills(file_path)
    
    suggestions = await suggest_skills_and_roles(skills)

    return {
        "message": "Resume uploaded successfully",
        "skills": skills,
        "suggested_skills": suggestions.get("suggested_skills", []),
        "suggested_roles": suggestions.get("suggested_roles", [])
    }

@app.post("/generate-questions")
async def get_questions(data: dict):

    skills = data.get("skills", [])
    role = data.get("role", "Software Engineer")
    difficulty = data.get("difficulty", "Medium")
    questions_count = data.get("questions_count", 10)

    try:
        questions = await generate_questions(skills, role, difficulty, questions_count)
        return {"questions": questions}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
def get_models():
    from google import genai
    import os
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return {"models": [m.name for m in client.models.list()]}

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

@app.post("/evaluate-interview")
async def evaluate_interview_endpoint(req: EvaluationRequest):
    try:
        if len(req.questions) == 0 or len(req.answers) == 0:
            return {"overall_score": 0, "feedback_summary": "No answers provided.", "detailed_analysis": []}
            
        evaluation_result = await evaluate_answers(req.questions, req.answers, req.role, req.skills)
        return evaluation_result
    except Exception as e:
        from fastapi import HTTPException
        print(f"Error evaluating interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Error evaluating interview")