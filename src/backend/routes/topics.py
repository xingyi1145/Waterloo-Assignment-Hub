"""
Topic management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Topic, Course
from ..schemas import TopicCreate, TopicResponse
from ..auth import get_current_user, get_current_professor

router = APIRouter()


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Create a new topic in a course (professors only)
    """
    # Verify course exists
    course = db.query(Course).filter(Course.id == topic_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Verify professor owns the course
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create topics in your own courses"
        )
    
    new_topic = Topic(
        title=topic_data.title,
        description=topic_data.description,
        course_id=topic_data.course_id
    )
    
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    
    return TopicResponse.from_orm(new_topic)


@router.get("/course/{course_id}", response_model=List[TopicResponse])
async def list_topics_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all topics for a specific course
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
                detail="You must be enrolled in this course to view topics"
            )
    
    topics = db.query(Topic).filter(Topic.course_id == course_id).all()
    return [TopicResponse.from_orm(topic) for topic in topics]


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific topic by ID
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    return TopicResponse.from_orm(topic)


@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Update a topic
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    topic.title = topic_data.title
    topic.description = topic_data.description
    
    db.commit()
    db.refresh(topic)
    return TopicResponse.from_orm(topic)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor)
):
    """
    Delete a topic
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    db.delete(topic)
    db.commit()
    return None
