from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User, LearnerProfile, Course
from backend.services.recommendation_service import build_personalized_plan

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/{course_id}")
def recommendations(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not profile:
        raise HTTPException(status_code=404, detail="Learner profile not found")

    return {
        "course": course.name,
        "recommendations": build_personalized_plan(profile, course.name),
    }
