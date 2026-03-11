import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User, ProgressStats, LearnerProfile

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stats = db.query(ProgressStats).filter(ProgressStats.user_id == current_user.id).first()
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()

    return {
        "weekly_learning_progress": json.loads(stats.weekly_progress or "[]") if stats else [],
        "topic_mastery_chart": json.loads(stats.topic_mastery or "{}") if stats else {},
        "strong_topics": json.loads(stats.strong_topics or "[]") if stats else [],
        "weak_topics": json.loads(stats.weak_topics or "[]") if stats else [],
        "learning_streak": current_user.streak_days,
        "progress_level": stats.progress_level if stats else "Level 1",
        "learning_speed": profile.learning_speed if profile else "moderate",
        "knowledge_level": profile.knowledge_level if profile else "beginner",
    }
