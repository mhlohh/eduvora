import json


def compute_learning_speed(avg_time_seconds: float) -> str:
    if avg_time_seconds <= 20:
        return "fast"
    if avg_time_seconds <= 45:
        return "moderate"
    return "slow"


def compute_knowledge_level(score: float) -> str:
    if score < 40:
        return "beginner"
    if score < 70:
        return "intermediate"
    return "advanced"


def build_learner_profile(quiz_payload: dict, topic_scores: dict, coding_errors: dict | None = None) -> dict:
    score = float(quiz_payload.get("score", 0))
    avg_time = float(quiz_payload.get("avg_time", 0))

    weak_topics = [t for t, s in topic_scores.items() if s < 50]
    strong_topics = [t for t, s in topic_scores.items() if s >= 75]

    # Penalize confidence level if coding errors are high
    if coding_errors and coding_errors.get("total", 0) >= 3 and score >= 70:
        score = 65

    return {
        "learning_speed": compute_learning_speed(avg_time),
        "knowledge_level": compute_knowledge_level(score),
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
    }


def parse_json_field(value: str, fallback):
    try:
        return json.loads(value)
    except Exception:
        return fallback
