from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class CodeSubmission(BaseModel):
    code: str
    test_cases: str
    question_id: int
    user_id: int  # Add user_id to track who submitted

class Question(BaseModel):
    id: int
    title: str
    description: str
    test_cases: str

    class Config:
        orm_mode = True

class SolutionResponse(BaseModel):
    passed: bool
    output: str
    error: str
    solution_id: int

    class Config:
        orm_mode = True
