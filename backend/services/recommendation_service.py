import json
from ai_engine.recommendation_engine import generate_recommendations
from ai_engine.learner_model import parse_json_field


def build_personalized_plan(profile_row, course_name: str):
    profile = {
        "learning_speed": profile_row.learning_speed,
        "knowledge_level": profile_row.knowledge_level,
    }
    weak_topics = parse_json_field(profile_row.weak_topics or "[]", [])
    return generate_recommendations(profile, course_name, weak_topics)
