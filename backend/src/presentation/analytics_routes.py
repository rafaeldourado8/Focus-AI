"""
Analytics Routes

Usage statistics and metrics
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.infrastructure.database.connection import get_db
from src.infrastructure.auth.auth_service import get_current_user
from src.infrastructure.database.models import LearningSessionModel, QuestionModel, AnswerModel
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats")
async def get_user_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user usage statistics"""
    user_id = current_user["user_id"]
    
    # Total sessions
    total_sessions = db.query(func.count(LearningSessionModel.id)).filter(
        LearningSessionModel.user_id == user_id
    ).scalar()
    
    # Total questions
    total_questions = db.query(func.count(QuestionModel.id)).join(
        LearningSessionModel
    ).filter(
        LearningSessionModel.user_id == user_id
    ).scalar()
    
    # Questions last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    questions_last_7d = db.query(func.count(QuestionModel.id)).join(
        LearningSessionModel
    ).filter(
        LearningSessionModel.user_id == user_id,
        QuestionModel.created_at >= seven_days_ago
    ).scalar()
    
    # Questions by day (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    questions_by_day = db.query(
        func.date(QuestionModel.created_at).label('date'),
        func.count(QuestionModel.id).label('count')
    ).join(
        LearningSessionModel
    ).filter(
        LearningSessionModel.user_id == user_id,
        QuestionModel.created_at >= thirty_days_ago
    ).group_by(
        func.date(QuestionModel.created_at)
    ).order_by(
        func.date(QuestionModel.created_at)
    ).all()
    
    return {
        "total_sessions": total_sessions or 0,
        "total_questions": total_questions or 0,
        "questions_last_7d": questions_last_7d or 0,
        "questions_by_day": [
            {"date": str(row.date), "count": row.count}
            for row in questions_by_day
        ]
    }

@router.get("/activity")
async def get_recent_activity(
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activity"""
    user_id = current_user["user_id"]
    
    recent_questions = db.query(QuestionModel).join(
        LearningSessionModel
    ).filter(
        LearningSessionModel.user_id == user_id
    ).order_by(
        QuestionModel.created_at.desc()
    ).limit(limit).all()
    
    return {
        "activities": [
            {
                "id": q.id,
                "content": q.content[:100] + "..." if len(q.content) > 100 else q.content,
                "created_at": q.created_at.isoformat() if q.created_at else None,
                "session_id": q.session_id
            }
            for q in recent_questions
        ]
    }
