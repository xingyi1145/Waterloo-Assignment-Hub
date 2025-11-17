"""
Solution submission and management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Solution, Question, Comment
from ..schemas import SolutionCreate, SolutionResponse, CommentCreate, CommentResponse
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=SolutionResponse, status_code=status.HTTP_201_CREATED)
async def submit_solution(
    solution_data: SolutionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a solution to a question
    """
    # Verify question exists
    question = db.query(Question).filter(Question.id == solution_data.question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    new_solution = Solution(
        question_id=solution_data.question_id,
        submitter_id=current_user.id,
        code=solution_data.code,
        language=solution_data.language,
        status="pending"  # Will be updated after testcase execution
    )
    
    db.add(new_solution)
    db.commit()
    db.refresh(new_solution)
    
    # TODO: Execute testcases here and update status
    
    return SolutionResponse.from_orm(new_solution)


@router.get("/question/{question_id}", response_model=List[SolutionResponse])
async def list_solutions_by_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all solutions for a specific question, sorted by likes
    """
    solutions = db.query(Solution).filter(
        Solution.question_id == question_id
    ).order_by(Solution.likes.desc()).all()
    
    return [SolutionResponse.from_orm(solution) for solution in solutions]


@router.get("/{solution_id}", response_model=SolutionResponse)
async def get_solution(
    solution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific solution by ID
    """
    solution = db.query(Solution).filter(Solution.id == solution_id).first()
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )
    
    return SolutionResponse.from_orm(solution)


@router.post("/{solution_id}/like", status_code=status.HTTP_200_OK)
async def like_solution(
    solution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Like a solution (one like per user)
    """
    solution = db.query(Solution).filter(Solution.id == solution_id).first()
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )
    
    # Check if user already liked this solution
    if solution in current_user.liked_solutions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this solution"
        )
    
    # Add user to liked_by_users
    current_user.liked_solutions.append(solution)
    solution.likes += 1
    db.commit()
    
    return {"message": "Solution liked", "likes": solution.likes}


@router.post("/{solution_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    solution_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a comment to a solution
    """
    solution = db.query(Solution).filter(Solution.id == solution_id).first()
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )
    
    new_comment = Comment(
        solution_id=solution_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse.from_orm(new_comment)


@router.get("/{solution_id}/comments", response_model=List[CommentResponse])
async def list_comments(
    solution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all comments for a solution
    """
    comments = db.query(Comment).filter(Comment.solution_id == solution_id).all()
    return [CommentResponse.from_orm(comment) for comment in comments]


@router.delete("/{solution_id}", status_code=status.HTTP_200_OK)
async def delete_solution(
    solution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a solution (owner or professor can delete)
    """
    solution = db.query(Solution).filter(Solution.id == solution_id).first()
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )
    
    # Check if user is the owner or a professor
    if solution.submitter_id != current_user.id and current_user.identity != 'professor':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own solutions (or any solution if you are a professor)"
        )
    
    # Manually clear likes (many-to-many relationship)
    solution.liked_by_users.clear()
    db.flush()  # Flush to ensure likes are deleted first
    
    db.delete(solution)
    db.commit()
    
    return {"message": "Solution deleted successfully"}
