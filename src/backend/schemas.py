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


# Topic Schemas
class TopicBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None


class TopicCreate(TopicBase):
    course_id: int


class TopicResponse(TopicBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Study Note Schemas
from enum import Enum

class ResourceType(str, Enum):
    CheatSheet = "CheatSheet"
    Summary = "Summary"
    Guide = "Guide"

class StudyNoteBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    summary: Optional[str] = Field(None, max_length=500)
    resource_type: ResourceType


class StudyNoteCreate(StudyNoteBase):
    topic_id: int


class StudyNoteResponse(StudyNoteBase):
    id: int
    topic_id: int
    author_id: int
    likes_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Comment Schemas
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    note_id: int


class CommentResponse(CommentBase):
    id: int
    note_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

