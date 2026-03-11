from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User
from backend.schemas.schemas import PersonalizationRequest

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/personalization")
def update_personalization(
    payload: PersonalizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.name = payload.name
    current_user.field_of_study = payload.field_of_study
    current_user.learning_interest = payload.learning_interest
    db.commit()
    return {"message": "Personalization saved"}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "field_of_study": current_user.field_of_study,
        "learning_interest": current_user.learning_interest,
        "streak_days": current_user.streak_days,
    }
