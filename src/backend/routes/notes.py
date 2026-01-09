"""
Study Note management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, StudyNote, Topic, Comment
from ..schemas import StudyNoteCreate, StudyNoteResponse, CommentCreate, CommentResponse
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=StudyNoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: StudyNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new study note
    """
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == note_data.topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    new_note = StudyNote(
        topic_id=note_data.topic_id,
        author_id=current_user.id,
        title=note_data.title,
        content=note_data.content,
        summary=note_data.summary,
        resource_type=note_data.resource_type
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return StudyNoteResponse.from_orm(new_note)


@router.get("/topic/{topic_id}", response_model=List[StudyNoteResponse])
async def list_notes_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all notes for a specific topic, sorted by likes
    """
    notes = db.query(StudyNote).filter(
        StudyNote.topic_id == topic_id
    ).order_by(StudyNote.likes_count.desc()).all()
    
    return [StudyNoteResponse.from_orm(note) for note in notes]


@router.get("/{note_id}", response_model=StudyNoteResponse)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific note by ID
    """
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study Note not found"
        )
    
    return StudyNoteResponse.from_orm(note)


@router.post("/{note_id}/like", status_code=status.HTTP_200_OK)
async def like_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Like a note (one like per user)
    """
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    if current_user in note.liked_by_users:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this note"
        )
    
    note.liked_by_users.append(current_user)
    note.likes_count += 1
    db.commit()
    
    return {"message": "Note liked successfully", "likes": note.likes_count}


@router.post("/{note_id}/comments", response_model=CommentResponse)
async def add_comment(
    note_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a comment to a note
    """
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    new_comment = Comment(
        note_id=note_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse.from_orm(new_comment)

@router.get("/{note_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    return [CommentResponse.from_orm(c) for c in note.comments]

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    # Check permissions (author or professor)
    if current_user.id != note.author_id and current_user.identity != 'professor':
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.delete(note)
    db.commit()
    return None
