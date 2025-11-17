"""
Database models for Waterloo CS Assignment Hub
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base


# Association table for user enrollments
user_courses = Table(
    'user_courses',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'))
)

# Association table for solution likes (track which users liked which solutions)
user_solution_likes = Table(
    'user_solution_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('solution_id', Integer, ForeignKey('solutions.id', ondelete='CASCADE'), primary_key=True)
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
    solutions = relationship("Solution", back_populates="submitter")
    liked_solutions = relationship("Solution", secondary=user_solution_likes, back_populates="liked_by_users")


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
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    assignment_name = Column(String(200), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    questions = relationship("Question", back_populates="assignment", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20))  # "easy", "medium", "hard"
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assignment = relationship("Assignment", back_populates="questions")
    testcases = relationship("Testcase", back_populates="question", cascade="all, delete-orphan")
    solutions = relationship("Solution", back_populates="question", cascade="all, delete-orphan")


class Testcase(Base):
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)  # Hidden test cases for evaluation
    
    # Relationships
    question = relationship("Question", back_populates="testcases")


class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    submitter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)  # "python", "java", "cpp"
    status = Column(String(20), default="pending")  # "pending", "passed", "failed"
    likes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("Question", back_populates="solutions")
    submitter = relationship("User", back_populates="solutions")
    comments = relationship("Comment", back_populates="solution", cascade="all, delete-orphan")
    liked_by_users = relationship("User", secondary="user_solution_likes", back_populates="liked_solutions")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey('solutions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    solution = relationship("Solution", back_populates="comments")
    user = relationship("User")
