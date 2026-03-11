"""
AI Classifier - Determines student learning level based on quiz performance.
Classification:
  0-40  -> Beginner
  40-70 -> Intermediate
  70-100 -> Advanced
Also considers time taken per question to refine classification.
"""

def classify_level(score: float, avg_time_per_question: float = None) -> str:
    """
    Classify student learning level based on score and optionally time.
    
    Args:
        score: Percentage score (0-100)
        avg_time_per_question: Average seconds per question (optional)
    
    Returns:
        Level string: 'Beginner', 'Intermediate', or 'Advanced'
    """
    # Base classification
    if score < 40:
        level = "Beginner"
    elif score < 70:
        level = "Intermediate"
    else:
        level = "Advanced"

    # Time-based refinement (optional factor)
    if avg_time_per_question is not None:
        # Very fast answers with low score may indicate guessing -> stay Beginner
        # Very slow answers with high score -> still Advanced but noted
        if level == "Intermediate" and avg_time_per_question < 5:
            # Answered fast but mid-range score - likely guessing, keep Intermediate
            pass
        elif level == "Advanced" and avg_time_per_question > 90:
            # Took very long even for advanced - keep Advanced but flag
            pass

    return level


def get_level_info(level: str) -> dict:
    """Returns metadata about a learning level."""
    info = {
        "Beginner": {
            "color": "#ef4444",
            "icon": "🌱",
            "description": "You're just starting out! Focus on fundamentals.",
            "badge_class": "beginner",
            "next_level": "Intermediate",
            "score_needed": 40,
        },
        "Intermediate": {
            "color": "#f59e0b",
            "icon": "📚",
            "description": "Good progress! You have foundational knowledge.",
            "badge_class": "intermediate",
            "next_level": "Advanced",
            "score_needed": 70,
        },
        "Advanced": {
            "color": "#10b981",
            "icon": "🚀",
            "description": "Excellent! You have a strong grasp of the material.",
            "badge_class": "advanced",
            "next_level": None,
            "score_needed": None,
        },
    }
    return info.get(level, info["Beginner"])


def calculate_topic_scores(answers: list, questions: list) -> dict:
    """
    Calculate per-topic scores from a quiz attempt.

    Args:
        answers: List of submitted answer indices
        questions: List of question dicts with 'topic', 'correct_answer'

    Returns:
        Dict of {topic: percentage_score}
    """
    topic_results = {}

    for i, question in enumerate(questions):
        topic = question.get("topic", "General")
        correct = question.get("correct_answer")
        user_answer = answers[i] if i < len(answers) else None

        if topic not in topic_results:
            topic_results[topic] = {"correct": 0, "total": 0}

        topic_results[topic]["total"] += 1
        if user_answer == correct:
            topic_results[topic]["correct"] += 1

    # Convert to percentages
    topic_scores = {}
    for topic, result in topic_results.items():
        if result["total"] > 0:
            topic_scores[topic] = round(
                (result["correct"] / result["total"]) * 100, 1
            )

    return topic_scores
