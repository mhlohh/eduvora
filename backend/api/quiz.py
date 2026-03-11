import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User, Course, QuizResult, LearnerProfile, ProgressStats
from backend.schemas.schemas import QuizSubmitRequest
from backend.services.quiz_service import generate_adaptive_quiz, score_quiz
from ai_engine.learner_model import build_learner_profile, parse_json_field

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.get("/diagnostic/{course_id}")
def diagnostic_quiz(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    questions = generate_adaptive_quiz(course.name)
    return {
        "course_id": course_id,
        "total_questions": 10,
        "base_questions": 5,
        "adaptive_questions": 5,
        "skip_limit": 2,
        "questions": questions,
    }


@router.post("/submit")
def submit_quiz(
    payload: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.id == payload.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    questions = generate_adaptive_quiz(course.name)
    scored = score_quiz(questions, payload.answers)
    if scored["skipped_questions"] > 2:
        raise HTTPException(status_code=400, detail="Skip limit exceeded (max 2)")

    qr = QuizResult(
        user_id=current_user.id,
        course_id=course.id,
        score=scored["score"],
        time_taken=int(scored["avg_time"] * max(scored["attempts"], 1)),
        skipped_questions=scored["skipped_questions"],
        attempts=scored["attempts"],
        payload=json.dumps(scored),
    )
    db.add(qr)

    learner = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not learner:
        learner = LearnerProfile(user_id=current_user.id)
        db.add(learner)

    profile = build_learner_profile(scored, scored["topic_scores"], None)
    learner.learning_speed = profile["learning_speed"]
    learner.knowledge_level = profile["knowledge_level"]
    learner.strong_topics = json.dumps(profile["strong_topics"])
    learner.weak_topics = json.dumps(profile["weak_topics"])
    learner.updated_at = datetime.utcnow()

    prog = db.query(ProgressStats).filter(ProgressStats.user_id == current_user.id).first()
    if not prog:
        prog = ProgressStats(user_id=current_user.id)
        db.add(prog)
    weekly = parse_json_field(prog.weekly_progress or "[]", [])
    weekly.append({"date": datetime.utcnow().strftime("%Y-%m-%d"), "score": scored["score"]})
    prog.weekly_progress = json.dumps(weekly[-7:])
    prog.topic_mastery = json.dumps(scored["topic_scores"])
    prog.strong_topics = json.dumps(profile["strong_topics"])
    prog.weak_topics = json.dumps(profile["weak_topics"])
    prog.progress_level = f"Level {'1' if profile['knowledge_level']=='beginner' else ('2' if profile['knowledge_level']=='intermediate' else '3')}"

    db.commit()

    return {
        "quiz_result": scored,
        "learner_profile": profile,
        "decision_logic": {
            "if_difficult": [
                "suggest easier material",
                "add introduction content",
                "recommend extra practice questions",
            ],
            "if_easy": ["skip basics", "move to advanced topics"],
            "if_struggles_basics": ["recommend revision modules"],
        },
    }
