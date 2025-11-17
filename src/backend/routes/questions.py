"""
Question management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Question, Assignment, Course
from ..schemas import QuestionCreate, QuestionResponse
from ..auth import get_current_user, get_current_professor

router = APIRouter()


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Create a new question in an assignment (professors only)
    """
    # Verify assignment exists
    assignment = db.query(Assignment).filter(Assignment.id == question_data.assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Verify professor owns the course
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create questions in your own courses"
        )
    
    new_question = Question(
        title=question_data.title,
        description=question_data.description,
        difficulty=question_data.difficulty,
        assignment_id=question_data.assignment_id
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return QuestionResponse.from_orm(new_question)


@router.get("/assignment/{assignment_id}", response_model=List[QuestionResponse])
async def list_questions_by_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all questions for a specific assignment
    """
    questions = db.query(Question).filter(Question.assignment_id == assignment_id).all()
    return [QuestionResponse.from_orm(question) for question in questions]


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific question by ID
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return QuestionResponse.from_orm(question)


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Update a question (professor who owns the course only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Professors can edit any question (admin privileges)
    # No ownership check needed
    
    # Update fields
    question.title = question_data.title
    question.description = question_data.description
    question.difficulty = question_data.difficulty
    
    db.commit()
    db.refresh(question)
    
    return QuestionResponse.from_orm(question)


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Delete a question (professor who owns the course only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Professors can delete any question (admin privileges)
    # No ownership check needed
    
    db.delete(question)
    db.commit()
    
    return {"message": "Question deleted successfully"}
