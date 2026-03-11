from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend.models.models import Course

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("")
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [
        {"id": c.id, "name": c.name, "description": c.description}
        for c in courses
    ]
