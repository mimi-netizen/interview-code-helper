from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import subprocess
import tempfile
import os

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    solutions = relationship("Solution", back_populates="user")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    test_cases = Column(String)
    solutions = relationship("Solution", back_populates="question")

class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    code = Column(String)
    passed = Column(Boolean)
    user = relationship("User", back_populates="solutions")
    question = relationship("Question", back_populates="solutions")

def evaluate_submission(db, submission):
    # Create a solution record
    solution = Solution(
        user_id=submission.user_id,
        question_id=submission.question_id,
        code=submission.code
    )
    
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        # Add print statements to capture output
        setup_code = "import sys\nfrom io import StringIO\nold_stdout = sys.stdout\nsys.stdout = StringIO()\n\n"
        f.write(setup_code.encode())
        f.write(submission.code.encode())
        f.write(b'\n')
        f.write(submission.test_cases.encode())
        f.write(b'\n\noutput = sys.stdout.getvalue()\nsys.stdout = old_stdout\nprint(output)')
    
    try:
        result = subprocess.run(['python', f.name], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        passed = result.returncode == 0
        output = result.stdout
        error = result.stderr
    except Exception as e:
        passed = False
        output = ""
        error = str(e)
    
    os.unlink(f.name)
    
    # Update solution record
    solution.passed = passed
    db.add(solution)
    db.commit()
    
    return {
        "passed": passed,
        "output": output,
        "error": error,
        "solution_id": solution.id
    }

def get_all_questions(db):
    questions = db.query(Question).all()
    return questions

def create_question(db, title: str, description: str, test_cases: str):
    db_question = Question(
        title=title,
        description=description,
        test_cases=test_cases
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
