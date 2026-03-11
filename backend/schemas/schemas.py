from typing import Any
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr | None = None
    mobile: str | None = None
    password: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    mobile: str | None = None
    password: str | None = None


class GoogleLoginRequest(BaseModel):
    id_token: str


class FirebaseLoginRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PersonalizationRequest(BaseModel):
    name: str
    field_of_study: str
    learning_interest: str


class QuizSubmitRequest(BaseModel):
    course_id: int
    answers: list[dict[str, Any]]


class CodeRunRequest(BaseModel):
    course_id: int
    language: str = "python"
    code: str
    test_cases: list[dict[str, Any]] = []


class TutorRequest(BaseModel):
    message: str
    context: dict[str, Any] | None = None
