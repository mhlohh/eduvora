import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User, LearnerProfile
from backend.schemas.schemas import TutorRequest
from backend.services.tutor_service import tutor_reply

router = APIRouter(prefix="/api/tutor", tags=["tutor"])


@router.post("/chat")
def chat(
    payload: TutorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    learner = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()

    weak_topics = []
    strong_topics = []
    knowledge_level = "beginner"
    learning_speed = "moderate"

    if learner:
        try:
            weak_topics = json.loads(learner.weak_topics or "[]")
        except Exception:
            weak_topics = []
        try:
            strong_topics = json.loads(learner.strong_topics or "[]")
        except Exception:
            strong_topics = []
        knowledge_level = learner.knowledge_level or "beginner"
        learning_speed = learner.learning_speed or "moderate"

    learner_context = {
        "knowledge_level": knowledge_level,
        "learning_speed": learning_speed,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "field_of_study": current_user.field_of_study or "",
        "learning_interest": current_user.learning_interest or "",
    }

    merged_context = {**learner_context, **(payload.context or {})}
    return tutor_reply(payload.message, merged_context, user_name=current_user.name)
