from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from . import models, schemas, database, auth
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Coder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=Dict[str, str])
def read_root():
    return {
        "status": "ok",
        "message": "Interview Coder API is running",
        "version": "1.0.0"
    }

@app.get("/debug/routes", response_model=List[Dict[str, str]])
def get_routes():
    """List all available routes for debugging"""
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "methods": ", ".join([method for method in route.methods]) if route.methods else "",
            "name": route.name if route.name else ""
        })
    return routes

@app.get("/debug/db", response_model=Dict[str, Any])
def check_db(db: Session = Depends(get_db)):
    """Check database status and counts"""
    try:
        user_count = db.query(models.User).count()
        question_count = db.query(models.Question).count()
        solution_count = db.query(models.Solution).count()
        return {
            "status": "connected",
            "counts": {
                "users": user_count,
                "questions": question_count,
                "solutions": solution_count
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"}
    )

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.authenticate_user(db, user.email, user.password)

@app.get("/questions", response_model=Dict[str, Any])
def get_questions(db: Session = Depends(get_db)):
    questions = models.get_all_questions(db)
    if not questions:
        # Add some sample questions if none exist
        sample_questions = [
            {
                "title": "Two Sum",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "test_cases": """
def test_solution():
    assert solution([2,7,11,15], 9) == [0,1]
    assert solution([3,2,4], 6) == [1,2]
"""
            },
            {
                "title": "Reverse String",
                "description": "Write a function that reverses a string.",
                "test_cases": """
def test_solution():
    assert solution("hello") == "olleh"
    assert solution("world") == "dlrow"
"""
            }
        ]
        for q in sample_questions:
            new_question = models.Question(**q)
            db.add(new_question)
        db.commit()
        questions = models.get_all_questions(db)
    
    return {
        "total": len(questions),
        "questions": questions
    }

@app.post("/submit")
def submit_solution(submission: schemas.CodeSubmission, db: Session = Depends(get_db)):
    return {"result": models.evaluate_submission(db, submission)}
