"""
Database models for Waterloo CS Study Note Hub
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


# Enum for resource type
class ResourceType(str, enum.Enum):
    CheatSheet = "CheatSheet"
    Summary = "Summary"
    Guide = "Guide"


# Association table for user enrollments
user_courses = Table(
    'user_courses',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'))
)

# Association table for note likes (track which users liked which notes)
user_note_likes = Table(
    'user_note_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('note_id', Integer, ForeignKey('study_notes.id', ondelete='CASCADE'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    identity = Column(String(20), nullable=False)  # "student" or "professor"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    enrolled_courses = relationship("Course", secondary=user_courses, back_populates="enrolled_students")
    created_courses = relationship("Course", back_populates="creator", foreign_keys="Course.creator_id")
    notes = relationship("StudyNote", back_populates="author")
    liked_notes = relationship("StudyNote", secondary=user_note_likes, back_populates="liked_by_users")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, index=True, nullable=False)  # e.g., "CS137"
    course_name = Column(String(200), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_courses", foreign_keys=[creator_id])
    enrolled_students = relationship("User", secondary=user_courses, back_populates="enrolled_courses")
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="topics")
    notes = relationship("StudyNote", back_populates="topic", cascade="all, delete-orphan")


class StudyNote(Base):
    __tablename__ = "study_notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    summary = Column(String(500), nullable=True)
    resource_type = Column(Enum(ResourceType), nullable=False)
    
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    topic = relationship("Topic", back_populates="notes")
    author = relationship("User", back_populates="notes")
    comments = relationship("Comment", back_populates="note", cascade="all, delete-orphan")
    liked_by_users = relationship("User", secondary=user_note_likes, back_populates="liked_notes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey('study_notes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    note = relationship("StudyNote", back_populates="comments")
    user = relationship("User")
