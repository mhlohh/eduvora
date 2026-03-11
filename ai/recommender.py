"""
Personalized Recommender - Maps weak areas + learning level to curated resources.
"""
from data.resources import RESOURCES

PREREQUISITE_TOPICS = {
    "Linear Regression": ["Machine Learning Basics"],
    "Classification": ["Machine Learning Basics", "Probability & Statistics"],
    "Neural Networks": ["Linear Algebra", "Machine Learning Basics"],
    "Decision Trees": ["Machine Learning Basics"],
    "Clustering": ["Machine Learning Basics", "Linear Algebra"],
    "Overfitting & Underfitting": ["Machine Learning Basics", "Linear Regression"],
}


def get_recommendations(level: str, weak_areas: list, limit: int = 5) -> list:
    """
    Get personalized learning recommendations.

    Args:
        level: Student level (Beginner/Intermediate/Advanced)
        weak_areas: List of weak topic names
        limit: Max recommendations per topic

    Returns:
        List of recommendation dicts
    """
    recommendations = []

    # First, add resources for weak areas
    for topic in weak_areas:
        topic_resources = RESOURCES.get(topic, [])
        level_filtered = [
            r for r in topic_resources
            if r.get("level") in (level, "All")
        ]
        if not level_filtered:
            level_filtered = topic_resources  # fallback to all

        for resource in level_filtered[:2]:  # max 2 per weak topic
            recommendations.append({**resource, "topic": topic, "priority": "high"})

    # Add prerequisite/easier topic resources for weak topics.
    covered_topics = set(weak_areas)
    for weak_topic in weak_areas:
        for prereq in PREREQUISITE_TOPICS.get(weak_topic, []):
            if prereq in covered_topics:
                continue
            prereq_resources = RESOURCES.get(prereq, [])
            prereq_match = [
                r for r in prereq_resources
                if r.get("level") in ("Beginner", "All", level)
            ]
            if prereq_match:
                recommendations.append({
                    **prereq_match[0],
                    "topic": prereq,
                    "priority": "normal",
                })
                covered_topics.add(prereq)

    # Fill remaining slots with general level-appropriate content.
    general = RESOURCES.get("General", [])
    level_general = [r for r in general if r.get("level") in (level, "All")]
    remaining = limit - len(recommendations)
    for resource in level_general[:remaining]:
        recommendations.append({**resource, "topic": "General", "priority": "normal"})

    return recommendations[:limit + 3]  # allow slight overflow for better UX


def get_topic_resources(topic: str, level: str) -> list:
    """Get resources for a specific topic filtered by level."""
    topic_resources = RESOURCES.get(topic, [])
    filtered = [r for r in topic_resources if r.get("level") in (level, "All")]
    return filtered if filtered else topic_resources


def get_level_roadmap(level: str) -> dict:
    """Get a structured learning roadmap for a level."""
    roadmaps = {
        "Beginner": {
            "title": "Beginner Learning Path",
            "description": "Master the fundamentals before moving to advanced topics.",
            "steps": [
                "Complete Introduction to Machine Learning",
                "Study Statistics & Probability basics",
                "Learn Python for Data Science",
                "Practice with simple Linear Regression",
                "Take practice quizzes daily",
            ],
            "estimated_time": "4-6 weeks",
        },
        "Intermediate": {
            "title": "Intermediate Learning Path",
            "description": "Build on your foundation with practical projects.",
            "steps": [
                "Deep dive into Classification algorithms",
                "Study Neural Network fundamentals",
                "Work on real datasets (Kaggle)",
                "Learn Decision Trees and Random Forests",
                "Build a complete ML pipeline project",
            ],
            "estimated_time": "6-8 weeks",
        },
        "Advanced": {
            "title": "Advanced Learning Path",
            "description": "Master complex concepts and cutting-edge techniques.",
            "steps": [
                "Study Deep Learning architectures",
                "Learn NLP and Transformers",
                "Contribute to open-source ML projects",
                "Study research papers on arXiv",
                "Build and deploy production ML models",
            ],
            "estimated_time": "8-12 weeks",
        },
    }
    return roadmaps.get(level, roadmaps["Beginner"])
