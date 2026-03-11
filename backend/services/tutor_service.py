import httpx
from backend.core.config import settings


def _build_system_prompt(profile: dict, user_name: str) -> str:
    return (
        "You are EduVora Tutor, a personalized education AI assistant. "
        f"Student name: {user_name}. "
        f"Knowledge level: {profile.get('knowledge_level', 'beginner')}. "
        f"Learning speed: {profile.get('learning_speed', 'moderate')}. "
        f"Weak topics: {', '.join(profile.get('weak_topics', [])) or 'None'}. "
        f"Strong topics: {', '.join(profile.get('strong_topics', [])) or 'None'}. "
        f"Field of study: {profile.get('field_of_study', 'N/A')}. "
        f"Learning interest: {profile.get('learning_interest', 'N/A')}. "
        "Rules: explain clearly with simple language first, then provide one concise example. "
        "When student struggles, give prerequisite revision steps. "
        "If question is coding-related, include debug approach and edge-case checklist. "
        "Keep answers practical and concise."
    )


def _gemini_chat(message: str, profile: dict, user_name: str) -> str | None:
    if not settings.gemini_api_key:
        return None

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
    )
    headers = {
        "Content-Type": "application/json",
    }

    system_instruction = _build_system_prompt(profile, user_name)

    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {
            "temperature": settings.tutor_temperature,
            "maxOutputTokens": settings.tutor_max_tokens,
        },
    }

    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts).strip()
            return text or None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None


def _practice_questions(message: str, profile: dict) -> list[str]:
    weak_topics = profile.get("weak_topics", []) or []
    if weak_topics:
        topic = weak_topics[0]
        return [
            f"What is the core intuition behind {topic}?",
            f"Solve a beginner-level problem on {topic}.",
        ]

    m = message.lower()
    if "python" in m or "code" in m:
        return [
            "Write a function and test edge cases (empty input, null, large input).",
            "How would you debug this in three steps?",
        ]
    return [
        "What is the difference between underfitting and overfitting?",
        "When should you use classification instead of regression?",
    ]


def _fallback_answer(message: str) -> str:
    m = message.lower()
    if "overfitting" in m:
        return (
            "Overfitting means the model memorizes training data and fails on unseen data. "
            "Use cross-validation, regularization, and simpler models."
        )
    if "regression" in m:
        return "Regression predicts continuous values. Linear Regression uses y = mx + b."
    if "error" in m or "bug" in m:
        return "Read the traceback, isolate the failing line, then test with minimal input and edge cases."
    return (
        "I can explain concepts, generate practice questions, and help debug coding mistakes. "
        "Ask a specific topic to get a focused answer."
    )


def tutor_reply(message: str, context: dict | None = None, user_name: str = "Student") -> dict:
    profile = context or {}
    answer = _gemini_chat(message, profile, user_name)
    mode = "gemini"
    if not answer:
        answer = _fallback_answer(message)
        mode = "fallback"

    return {
        "answer": answer,
        "practice_questions": _practice_questions(message, profile),
        "mode": mode,
        "personalization_used": {
            "knowledge_level": profile.get("knowledge_level", "beginner"),
            "learning_speed": profile.get("learning_speed", "moderate"),
            "weak_topics": profile.get("weak_topics", []),
        },
    }
