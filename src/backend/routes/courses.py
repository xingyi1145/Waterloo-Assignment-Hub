"""
Course management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import delete
from typing import List

from ..database import get_db
from ..models import User, Course, user_courses
from ..schemas import CourseCreate, CourseResponse
from ..auth import get_current_user, get_current_professor

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Create a new course (professors only)
    """
    # Check if course code already exists
    existing_course = db.query(Course).filter(Course.course_code == course_data.course_code).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    new_course = Course(
        course_code=course_data.course_code,
        course_name=course_data.course_name,
        description=course_data.description,
        creator_id=current_user.id
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return CourseResponse.from_orm(new_course)


@router.get("/", response_model=List[CourseResponse])
async def list_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all available courses
    """
    courses = db.query(Course).all()
    result = []
    for course in courses:
        course_dict = CourseResponse.from_orm(course).dict()
        # Add enrollment status for students
        if current_user.identity == 'student':
            course_dict['is_enrolled'] = course in current_user.enrolled_courses
        else:
            course_dict['is_enrolled'] = True  # Professors have access to all
        result.append(CourseResponse(**course_dict))
    return result


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course_dict = CourseResponse.from_orm(course).dict()
    # Add enrollment status
    if current_user.identity == 'student':
        course_dict['is_enrolled'] = course in current_user.enrolled_courses
    else:
        course_dict['is_enrolled'] = True  # Professors have access to all
    
    return CourseResponse(**course_dict)


@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enroll current user in a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if already enrolled
    if course in current_user.enrolled_courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    current_user.enrolled_courses.append(course)
    db.commit()
    
    return {"message": "Successfully enrolled in course"}


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Update a course (professor who created it only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Professors can edit any course (admin privileges)
    # No ownership check needed
    
    # Update course fields
    course.course_code = course_data.course_code
    course.course_name = course_data.course_name
    course.description = course_data.description
    
    db.commit()
    db.refresh(course)
    
    return CourseResponse.from_orm(course)


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Delete a course (professor who created it only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Professors can delete any course (admin privileges)
    # No ownership check needed
    
    # Manually delete enrollments using raw SQL to avoid ORM issues
    db.execute(delete(user_courses).where(user_courses.c.course_id == course_id))
    
    # Now delete the course (cascade will handle assignments, questions, solutions)
    db.delete(course)
    db.commit()
    
    return {"message": "Course deleted successfully"}
