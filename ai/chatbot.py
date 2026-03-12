"""
AI Study Assistant Chatbot - Powered by local Ollama (DeepSeek R1).
Falls back to rule-based responses if Ollama is unavailable.
"""
import os
import ollama
from dotenv import load_dotenv

load_dotenv()

# Configure Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1")

# Standardize the client
_client = None
try:
    _client = ollama.Client(host=OLLAMA_BASE_URL)
except Exception as e:
    print(f"Ollama connection error: {e}")

SYSTEM_PROMPT = """You are EduBot, an AI Study Assistant for an online Learning Management System called EduVora.
You are a friendly, encouraging, and highly knowledgeable tutor specializing in:
- Machine Learning & AI
- Data Science & Statistics
- Mathematics (Linear Algebra, Probability)
- Programming (Python for ML)

Your role:
1. Answer student questions clearly and simply
2. Explain complex concepts using analogies and examples
3. Suggest relevant learning resources when appropriate
4. Encourage students and track their progress
5. If asked about a topic outside your expertise, gently redirect

Response guidelines:
- Keep responses concise (3-5 sentences max for simple questions)
- Use bullet points for step-by-step explanations
- Always be encouraging and positive
- Use emojis sparingly to be friendly
- If a student is struggling, suggest they review prerequisites first"""

# Rule-based fallback responses
FALLBACK_RESPONSES = {
    "overfitting": "**Overfitting** occurs when a model learns the training data too well, including noise and random fluctuations, causing it to perform poorly on new, unseen data. 📊\n\nThink of it like memorizing exam answers vs. truly understanding the subject. The model 'memorizes' training examples instead of learning general patterns.\n\n**Solutions:** Use cross-validation, add regularization (L1/L2), reduce model complexity, or get more training data.",
    "underfitting": "**Underfitting** happens when a model is too simple to capture the underlying patterns in the data. It performs poorly on both training and test data. 📉\n\nIt's like using a straight line to model a curved relationship.\n\n**Solutions:** Increase model complexity, add more features, reduce regularization, or train for more epochs.",
    "gradient descent": "**Gradient Descent** is an optimization algorithm used to minimize the loss function in ML models. 🎯\n\nImagine you're blindfolded on a hilly terrain trying to reach the lowest valley. At each step, you feel the slope and move in the downhill direction.\n\n**Types:** Batch GD, Stochastic GD (SGD), Mini-batch GD — each differs in how much data is used per update.",
    "neural network": "A **Neural Network** is a computational model inspired by the human brain, consisting of layers of interconnected nodes (neurons). 🧠\n\n**Structure:** Input Layer → Hidden Layers → Output Layer\n\nEach neuron receives inputs, applies weights, adds a bias, passes through an activation function, and sends output to the next layer. Training uses backpropagation to adjust weights and minimize prediction error.",
    "linear regression": "**Linear Regression** is a supervised ML algorithm that models the relationship between variables using a straight line (y = mx + b). 📈\n\nIt's used to predict continuous values (e.g., house prices, temperature).\n\n**Key concepts:** Minimize Mean Squared Error (MSE), the slope (m) shows the relationship strength, R² measures how well the line fits the data.",
    "classification": "**Classification** is a supervised ML task where the goal is to predict which category (class) an input belongs to. 🏷️\n\n**Examples:** Spam detection (spam/not spam), disease diagnosis (positive/negative), digit recognition (0-9).\n\n**Popular algorithms:** Logistic Regression, Decision Trees, Random Forest, SVM, Neural Networks.",
    "decision tree": "A **Decision Tree** is a flowchart-like model that makes decisions based on feature values. 🌳\n\nAt each node, it asks a yes/no question about a feature. The data is split based on the answer until reaching a leaf node (final prediction).\n\n**Key concepts:** Gini Impurity, Information Gain, Entropy — these measure how 'pure' each split is.",
    "clustering": "**Clustering** is an unsupervised ML technique that groups similar data points together without predefined labels. 🔵🟣🟡\n\n**K-Means Algorithm:** Choose K clusters → randomly place centroids → assign points to nearest centroid → move centroids to mean of cluster → repeat until stable.\n\n**Use cases:** Customer segmentation, anomaly detection, image compression.",
    "bias variance": "The **Bias-Variance Tradeoff** is fundamental in ML:\n\n- **High Bias (Underfitting):** Model is too simple, misses patterns\n- **High Variance (Overfitting):** Model is too complex, fits noise\n- **Goal:** Find the sweet spot with low bias AND low variance\n\nRegularization helps control variance. More data or better features help reduce bias.",
    "regularization": "**Regularization** adds a penalty to the model's complexity to prevent overfitting. ⚖️\n\n**L1 (Lasso):** Adds |weights| penalty — can make weights exactly zero (feature selection)\n\n**L2 (Ridge):** Adds weights² penalty — shrinks weights but rarely to zero\n\n**Elastic Net:** Combines L1 + L2 for the best of both worlds.",
    "ai engineer": "**AI Engineer Roadmap (Beginner to Job-Ready)** 🚀\n\n1. **Foundations (4-6 weeks):** Python, statistics, linear algebra, probability.\n2. **Core ML (6-8 weeks):** Supervised/unsupervised learning, model evaluation, feature engineering.\n3. **Deep Learning (6-8 weeks):** Neural networks, CNNs, transformers, fine-tuning basics.\n4. **Projects (ongoing):** Build 3-5 end-to-end projects (data -> model -> API -> UI).\n5. **MLOps & Deployment (4-6 weeks):** FastAPI, Docker, CI/CD, monitoring, cloud basics.\n6. **Portfolio + Interview Prep:** GitHub README, case studies, ML system design, coding practice.\n\n**Start today:** Pick one domain (NLP/CV/recommendation), build one small project, and ship weekly.",
    "roadmap": "**Structured Learning Path** 🗺️\n\n- **Phase 1:** Fundamentals (Python + Math + Stats)\n- **Phase 2:** Machine Learning basics + practice datasets\n- **Phase 3:** Deep Learning + specialization track\n- **Phase 4:** Deployment + MLOps + production mindset\n- **Phase 5:** Portfolio, resume, interview prep\n\nIf you tell me your current level and time per week, I can generate a personalized 30/60/90-day plan.",
    "learning path": "**Personal Learning Path Template** 📚\n\n- Week 1-2: Python + data handling\n- Week 3-4: Statistics + probability essentials\n- Week 5-8: ML algorithms + evaluation\n- Week 9-12: Projects + deployment\n\nShare your goal (job/exam/project), and I will tailor this plan.",
}


def get_rule_based_response(message: str) -> str | None:
    """Check if message matches a known topic and return a canned response."""
    message_lower = message.lower()
    for keyword, response in FALLBACK_RESPONSES.items():
        if keyword in message_lower:
            return response
    return None


def chat(message: str, history: list = None) -> str:
    """
    Send a message to EduBot (Ollama) and get a response.

    Args:
        message: User's question/message
        history: List of previous messages [{"role": "user/assistant", "content": "..."}]

    Returns:
        Bot response string
    """
    if _client:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            if history:
                for msg in history[-6:]:
                    # Ensure role matches Ollama/standard expectations (user/assistant)
                    role = "assistant" if msg["role"] in ("model", "assistant") else "user"
                    messages.append({"role": role, "content": msg["content"]})
            
            messages.append({"role": "user", "content": message})

            response = _client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "num_predict": 512,
                }
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama chat error: {e}")

    # Rule-based fallback
    rule_response = get_rule_based_response(message)
    if rule_response:
        return rule_response

    # Generic fallback
    return (
        "I'm here to help you learn! 🎓 I specialize in Machine Learning, Data Science, "
        "Statistics, and Python. Could you ask me about a specific concept? "
        "For example: 'What is overfitting?' or 'Explain gradient descent.'"
    )
