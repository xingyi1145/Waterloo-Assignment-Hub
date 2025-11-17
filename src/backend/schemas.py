"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    identity: str = Field(..., pattern="^(student|professor)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Course Schemas
class CourseBase(BaseModel):
    course_code: str = Field(..., max_length=20)
    course_name: str = Field(..., max_length=200)
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    creator_id: int
    created_at: datetime
    is_enrolled: Optional[bool] = None

    class Config:
        from_attributes = True


# Assignment Schemas
class AssignmentBase(BaseModel):
    assignment_name: str = Field(..., max_length=200)
    description: Optional[str] = None


class AssignmentCreate(AssignmentBase):
    course_id: int


class AssignmentResponse(AssignmentBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")


class QuestionCreate(QuestionBase):
    assignment_id: int


class QuestionResponse(QuestionBase):
    id: int
    assignment_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Testcase Schemas
class TestcaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False


class TestcaseCreate(TestcaseBase):
    question_id: int


class TestcaseResponse(TestcaseBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True


# Solution Schemas
class SolutionBase(BaseModel):
    code: str
    language: str = Field(..., pattern="^(python|java|cpp|javascript)$")


class SolutionCreate(SolutionBase):
    question_id: int


class SolutionResponse(SolutionBase):
    id: int
    question_id: int
    submitter_id: int
    status: str
    likes: int
    created_at: datetime

    class Config:
        from_attributes = True


# Comment Schemas
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    solution_id: int


class CommentResponse(CommentBase):
    id: int
    solution_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
