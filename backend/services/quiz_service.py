import random

TOPICS_BY_COURSE = {
    "Mathematics": ["Algebra", "Calculus", "Probability", "Geometry"],
    "Python": ["Syntax", "Loops", "Functions", "Data Structures"],
    "Machine Learning": ["ML Basics", "Regression", "Classification", "Data Preprocessing"],
    "Crash Course": ["Fundamentals", "Practice", "Revision", "Assessment"],
    "Test Mode": ["General Aptitude", "Reasoning", "Quantitative", "Verbal"],
}


def generate_adaptive_quiz(course_name: str) -> list[dict]:
    topics = TOPICS_BY_COURSE.get(course_name, ["General"])
    questions = []

    # First 5 base questions
    for i in range(5):
        topic = topics[i % len(topics)]
        questions.append(
            {
                "id": f"base_{i+1}",
                "topic": topic,
                "difficulty": "base",
                "question": f"[{topic}] Base question {i+1}",
                "options": ["A", "B", "C", "D"],
                "correct_answer": random.randint(0, 3),
                "allow_skip": True,
            }
        )

    # Next 5 adaptive questions
    for i in range(5):
        topic = topics[(i + 1) % len(topics)]
        questions.append(
            {
                "id": f"adaptive_{i+1}",
                "topic": topic,
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "question": f"[{topic}] Adaptive question {i+1}",
                "options": ["A", "B", "C", "D"],
                "correct_answer": random.randint(0, 3),
                "allow_skip": True,
            }
        )

    return questions


def score_quiz(questions: list[dict], answers: list[dict]) -> dict:
    qmap = {q["id"]: q for q in questions}
    correct = 0
    skipped = 0
    total_time = 0
    attempts = len(answers)
    topic_perf = {}

    for ans in answers:
        qid = ans.get("question_id")
        if qid not in qmap:
            continue
        q = qmap[qid]
        topic = q["topic"]
        topic_perf.setdefault(topic, {"correct": 0, "total": 0})

        selected = ans.get("selected")
        elapsed = int(ans.get("time_taken", 0))
        total_time += elapsed

        if selected is None:
            skipped += 1
            continue

        topic_perf[topic]["total"] += 1
        if selected == q["correct_answer"]:
            correct += 1
            topic_perf[topic]["correct"] += 1

    total_questions = len(questions)
    score = round((correct / total_questions) * 100, 2) if total_questions else 0
    avg_time = round(total_time / max(attempts, 1), 2)

    topic_scores = {}
    for topic, d in topic_perf.items():
        if d["total"] == 0:
            topic_scores[topic] = 0
        else:
            topic_scores[topic] = round((d["correct"] / d["total"]) * 100, 2)

    return {
        "score": score,
        "correct": correct,
        "total": total_questions,
        "skipped_questions": skipped,
        "avg_time": avg_time,
        "attempts": attempts,
        "topic_scores": topic_scores,
    }
