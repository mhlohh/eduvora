from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship
from backend.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    mobile = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    field_of_study = Column(String(120), nullable=True)
    learning_interest = Column(String(120), nullable=True)
    streak_days = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, default="")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(150), nullable=False)
    sequence = Column(Integer, default=1)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String(150), nullable=False)
    video_url = Column(String(255), default="")
    notes = Column(Text, default="")
    revision = Column(Text, default="")
    practice_questions = Column(Text, default="[]")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    score = Column(Float, default=0)
    time_taken = Column(Integer, default=0)
    skipped_questions = Column(Integer, default=0)
    attempts = Column(Integer, default=1)
    payload = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)


class LearnerProfile(Base):
    __tablename__ = "learner_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    learning_speed = Column(String(50), default="moderate")
    knowledge_level = Column(String(50), default="beginner")
    strong_topics = Column(Text, default="[]")
    weak_topics = Column(Text, default="[]")
    updated_at = Column(DateTime, default=datetime.utcnow)


class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    score = Column(Float, default=0)
    attempts = Column(Integer, default=1)
    weak = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    language = Column(String(30), default="python")
    code = Column(Text, nullable=False)
    result = Column(Text, default="{}")
    syntax_errors = Column(Integer, default=0)
    logic_errors = Column(Integer, default=0)
    attempts = Column(Integer, default=1)
    execution_success = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProgressStats(Base):
    __tablename__ = "progress_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    weekly_progress = Column(Text, default="[]")
    topic_mastery = Column(Text, default="{}")
    strong_topics = Column(Text, default="[]")
    weak_topics = Column(Text, default="[]")
    progress_level = Column(String(50), default="Level 1")
    updated_at = Column(DateTime, default=datetime.utcnow)
