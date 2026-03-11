def generate_recommendations(profile: dict, course_name: str, weak_topics: list[str]) -> list[dict]:
    recs = []
    level = profile.get("knowledge_level", "beginner")

    for topic in weak_topics:
        recs.append(
            {
                "type": "easier_material",
                "topic": topic,
                "title": f"Introduction to {topic}",
                "reason": "Topic is currently difficult based on quiz and attempts.",
            }
        )
        recs.append(
            {
                "type": "practice",
                "topic": topic,
                "title": f"Extra practice questions for {topic}",
                "reason": "Practice improves retention and confidence.",
            }
        )

    if level == "advanced":
        recs.append(
            {
                "type": "advanced",
                "topic": course_name,
                "title": f"Skip basics and move to advanced {course_name}",
                "reason": "Performance indicates mastery of fundamentals.",
            }
        )
    elif level == "beginner":
        recs.append(
            {
                "type": "revision",
                "topic": course_name,
                "title": "Revision module for fundamentals",
                "reason": "You are struggling with basic concepts.",
            }
        )

    return recs[:10]
