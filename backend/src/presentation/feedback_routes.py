"""
Feedback Routes

User feedback on answers
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from src.infrastructure.database.connection import get_db
from src.infrastructure.auth.auth_service import get_current_user
from src.infrastructure.database.models import AnswerModel, LearningSessionModel, QuestionModel
from datetime import datetime
import uuid

router = APIRouter()

class FeedbackRequest(BaseModel):
    answer_id: str
    rating: int  # 1-5
    comment: str = None

@router.post("/")
async def submit_feedback(
    request: FeedbackRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback for an answer"""
    
    # Validate rating
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    # Verify answer belongs to user
    answer = db.query(AnswerModel).join(
        QuestionModel
    ).join(
        LearningSessionModel
    ).filter(
        AnswerModel.id == request.answer_id,
        LearningSessionModel.user_id == current_user["user_id"]
    ).first()
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found or not authorized"
        )
    
    # Create feedback (simple insert - no entity for now)
    feedback_id = str(uuid.uuid4())
    db.execute(
        text("""
        INSERT INTO answer_feedback (id, answer_id, rating, comment, created_at)
        VALUES (:id, :answer_id, :rating, :comment, :created_at)
        """),
        {
            "id": feedback_id,
            "answer_id": request.answer_id,
            "rating": request.rating,
            "comment": request.comment,
            "created_at": datetime.utcnow()
        }
    )
    db.commit()
    
    return {
        "id": feedback_id,
        "message": "Feedback submitted successfully"
    }
