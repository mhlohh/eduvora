"""
Smart Quiz Generator - Dynamically generates quizzes based on topic and level.
Pulls questions from the question bank filtered by topic/level.
"""
import random
from data.questions import QUESTION_BANK


def generate_quiz(
    topic: str = None,
    level: str = None,
    weak_areas: list = None,
    num_questions: int = 10,
) -> list:
    """
    Generate a quiz dynamically.

    Args:
        topic: Specific topic to quiz on (None = all topics)
        level: Student level to set difficulty (Beginner/Intermediate/Advanced)
        weak_areas: List of weak topics to prioritize
        num_questions: Number of questions to generate

    Returns:
        List of question dicts
    """
    pool = list(QUESTION_BANK)

    # Filter by topic if specified
    if topic and topic != "diagnostic":
        pool = [q for q in pool if q.get("topic") == topic]

    # Filter by difficulty/level
    if level:
        level_map = {
            "Beginner": ["easy"],
            "Intermediate": ["easy", "medium"],
            "Advanced": ["medium", "hard"],
        }
        allowed_difficulties = level_map.get(level, ["easy", "medium", "hard"])
        pool = [q for q in pool if q.get("difficulty", "medium") in allowed_difficulties]

    # Prioritize weak area questions
    if weak_areas:
        weak_pool = [q for q in pool if q.get("topic") in weak_areas]
        other_pool = [q for q in pool if q.get("topic") not in weak_areas]

        # Take 70% from weak areas, 30% from others
        weak_count = min(int(num_questions * 0.7), len(weak_pool))
        other_count = min(num_questions - weak_count, len(other_pool))

        selected = random.sample(weak_pool, weak_count) + random.sample(
            other_pool, other_count
        )
    else:
        count = min(num_questions, len(pool))
        selected = random.sample(pool, count)

    # Shuffle final selection
    random.shuffle(selected)
    return selected


def generate_diagnostic_quiz() -> list:
    """Generate a balanced diagnostic quiz covering all topics."""
    topics = [
        "Machine Learning Basics",
        "Linear Regression",
        "Classification",
        "Probability & Statistics",
        "Linear Algebra",
        "Data Preprocessing",
        "Overfitting & Underfitting",
        "Neural Networks",
        "Decision Trees",
        "Clustering",
    ]

    selected = []
    for topic in topics:
        topic_questions = [q for q in QUESTION_BANK if q.get("topic") == topic]
        if topic_questions:
            # Pick 1 easy question per topic for diagnostic
            easy = [q for q in topic_questions if q.get("difficulty") == "easy"]
            if easy:
                selected.append(random.choice(easy))
            else:
                selected.append(random.choice(topic_questions))

    random.shuffle(selected)
    return selected[:10]  # Cap at 10 questions
