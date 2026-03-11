from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend.core.security import hash_password, verify_password, create_access_token
from backend.core.config import settings
from backend.core.firebase import verify_firebase_token
from backend.models.models import User, LearnerProfile, ProgressStats
from backend.schemas.schemas import (
    RegisterRequest,
    LoginRequest,
    GoogleLoginRequest,
    FirebaseLoginRequest,
    TokenResponse,
)
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if not payload.email and not payload.mobile:
        raise HTTPException(status_code=400, detail="Email or mobile is required")

    exists = db.query(User).filter(
        (User.email == payload.email) | (User.mobile == payload.mobile)
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        mobile=payload.mobile,
        password_hash=hash_password(payload.password or "pass@1234"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(LearnerProfile(user_id=user.id))
    db.add(ProgressStats(user_id=user.id))
    db.commit()

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == payload.email) | (User.mobile == payload.mobile)
    ).first()
    if not user or not verify_password(payload.password or "", user.password_hash or ""):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/google", response_model=TokenResponse)
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    email = None
    name = "Google Learner"

    try:
        if settings.google_client_id:
            info = google_id_token.verify_oauth2_token(
                payload.id_token,
                google_requests.Request(),
                settings.google_client_id,
            )
        else:
            info = google_id_token.verify_oauth2_token(
                payload.id_token,
                google_requests.Request(),
            )
        email = info.get("email")
        name = info.get("name") or name
    except Exception:
        if settings.allow_insecure_google_fallback:
            email = f"google_user_{payload.id_token[:8]}@eduvora.ai"
        else:
            raise HTTPException(status_code=401, detail="Invalid Google token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, password_hash=hash_password("google-auth"))
        db.add(user)
        db.commit()
        db.refresh(user)
        db.add(LearnerProfile(user_id=user.id))
        db.add(ProgressStats(user_id=user.id))
        db.commit()

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/firebase", response_model=TokenResponse)
def firebase_login(payload: FirebaseLoginRequest, db: Session = Depends(get_db)):
    decoded = verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid Firebase token or Firebase not configured")

    uid = decoded.get("uid", "")
    email = decoded.get("email")
    name = decoded.get("name") or "Firebase Learner"

    if not email:
        email = f"{uid}@firebase.local"

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, password_hash=hash_password("firebase-auth"))
        db.add(user)
        db.commit()
        db.refresh(user)
        db.add(LearnerProfile(user_id=user.id))
        db.add(ProgressStats(user_id=user.id))
        db.commit()

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)
