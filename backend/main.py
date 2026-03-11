from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from backend.core.db import Base, engine, SessionLocal
from backend.api import auth, users, courses, quiz, recommendations, dashboard, tutor, code
from backend.models.models import Course

app = FastAPI(title="EduVora API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Course).count()
        if existing == 0:
            db.add_all(
                [
                    Course(name="Mathematics", description="Numbers, algebra, and problem solving"),
                    Course(name="Python", description="Programming from basics to advanced"),
                    Course(name="Machine Learning", description="Models, evaluation, deployment"),
                    Course(name="Crash Course", description="Quick fundamentals"),
                    Course(name="Test Mode", description="Assessment only mode"),
                ]
            )
            db.commit()
    finally:
        db.close()


@app.get("/api/health")
def health():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(quiz.router)
app.include_router(recommendations.router)
app.include_router(dashboard.router)
app.include_router(tutor.router)
app.include_router(code.router)
