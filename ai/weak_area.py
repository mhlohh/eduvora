"""
Weak Area Detection - Identifies topics where the student struggles most.
Topics with < 50% score are flagged as weak areas.
"""

WEAK_THRESHOLD = 50  # percentage below which a topic is considered weak


def detect_weak_areas(topic_scores: dict) -> list:
    """
    Detect weak topics from per-topic scores.

    Args:
        topic_scores: Dict of {topic: percentage_score}

    Returns:
        List of weak topic names sorted by score (weakest first)
    """
    weak = []
    for topic, score in topic_scores.items():
        if score < WEAK_THRESHOLD:
            weak.append({"topic": topic, "score": score})

    # Sort weakest first
    weak.sort(key=lambda x: x["score"])
    return [item["topic"] for item in weak]


def get_weak_area_summary(topic_scores: dict) -> dict:
    """
    Returns a full summary of topic performance.

    Returns:
        {
            'weak': [...],
            'average': [...],
            'strong': [...]
        }
    """
    result = {"weak": [], "average": [], "strong": []}

    for topic, score in topic_scores.items():
        if score < 40:
            result["weak"].append({"topic": topic, "score": score})
        elif score < 70:
            result["average"].append({"topic": topic, "score": score})
        else:
            result["strong"].append({"topic": topic, "score": score})

    # Sort each group
    for key in result:
        result[key].sort(key=lambda x: x["score"])

    return result


def get_improvement_tips(weak_topics: list) -> list:
    """
    Returns structured improvement tips for weak topics.
    """
    tips_map = {
        "Machine Learning Basics": "Start with the definition of ML, supervised vs unsupervised learning.",
        "Linear Regression": "Practice drawing best-fit lines. Understand MSE loss function.",
        "Classification": "Study decision boundaries. Practice with binary classification examples.",
        "Probability & Statistics": "Review Bayes theorem, normal distribution, and hypothesis testing.",
        "Linear Algebra": "Focus on matrix multiplication, dot products, and eigenvectors.",
        "Data Preprocessing": "Learn about normalization, handling missing values, and feature encoding.",
        "Overfitting & Underfitting": "Understand bias-variance tradeoff and regularization techniques.",
        "Neural Networks": "Start with perceptron basics, then activation functions and backpropagation.",
        "Decision Trees": "Understand Gini impurity, entropy, and information gain.",
        "Clustering": "Study K-Means algorithm, centroids, and distance metrics.",
    }

    tips = []
    for topic in weak_topics:
        tip = tips_map.get(topic, f"Review the fundamentals of {topic}.")
        tips.append({"topic": topic, "tip": tip})
    return tips
