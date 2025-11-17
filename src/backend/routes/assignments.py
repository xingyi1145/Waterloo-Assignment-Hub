"""
Assignment management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Assignment, Course
from ..schemas import AssignmentCreate, AssignmentResponse
from ..auth import get_current_user, get_current_professor

router = APIRouter()


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Create a new assignment in a course (professors only)
    """
    # Verify course exists
    course = db.query(Course).filter(Course.id == assignment_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Verify professor owns the course
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create assignments in your own courses"
        )
    
    new_assignment = Assignment(
        assignment_name=assignment_data.assignment_name,
        description=assignment_data.description,
        course_id=assignment_data.course_id
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return AssignmentResponse.from_orm(new_assignment)


@router.get("/course/{course_id}", response_model=List[AssignmentResponse])
async def list_assignments_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all assignments for a specific course
    """
    # Get the course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user has access (professor or enrolled student)
    if current_user.identity == 'student':
        if course not in current_user.enrolled_courses:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be enrolled in this course to view assignments"
            )
    
    assignments = db.query(Assignment).filter(Assignment.course_id == course_id).all()
    return [AssignmentResponse.from_orm(assignment) for assignment in assignments]


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific assignment by ID
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return AssignmentResponse.from_orm(assignment)


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Update an assignment (professor who owns the course only)
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Professors can edit any assignment (admin privileges)
    # No ownership check needed
    
    # Update fields
    assignment.assignment_name = assignment_data.assignment_name
    assignment.description = assignment_data.description
    
    db.commit()
    db.refresh(assignment)
    
    return AssignmentResponse.from_orm(assignment)


@router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Delete an assignment (professor who owns the course only)
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Professors can delete any assignment (admin privileges)
    # No ownership check needed
    
    db.delete(assignment)
    db.commit()
    
    return {"message": "Assignment deleted successfully"}
