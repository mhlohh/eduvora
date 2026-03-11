"""
AI Study Assistant Chatbot - Powered by Google Gemini.
Falls back to rule-based responses if API is unavailable.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini — try new SDK first, fall back to old
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
_genai = None
_use_new_sdk = False

if GEMINI_API_KEY:
    try:
        from google import genai as new_genai
        _client = new_genai.Client(api_key=GEMINI_API_KEY)
        _use_new_sdk = True
    except Exception:
        try:
            import google.generativeai as old_genai
            old_genai.configure(api_key=GEMINI_API_KEY)
            _genai = old_genai
        except Exception:
            pass

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
    Send a message to EduBot and get a response.

    Args:
        message: User's question/message
        history: List of previous messages [{"role": "user/model", "content": "..."}]

    Returns:
        Bot response string
    """
    # Try new google.genai SDK
    if GEMINI_API_KEY and _use_new_sdk:
        try:
            from google import genai as new_genai
            from google.genai import types as genai_types

            contents = []
            if history:
                for msg in history[-6:]:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(
                        genai_types.Content(role=role, parts=[genai_types.Part(text=msg["content"])])
                    )
            contents.append(
                genai_types.Content(role="user", parts=[genai_types.Part(text=message)])
            )

            client = new_genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=512,
                ),
            )
            return response.text
        except Exception as e:
            print(f"Gemini (new SDK) error: {e}")

    # Try old google.generativeai SDK
    if GEMINI_API_KEY and _genai:
        try:
            model = _genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
            )
            chat_history = []
            if history:
                for msg in history[-6:]:
                    chat_history.append({
                        "role": msg["role"],
                        "parts": [msg["content"]],
                    })
            chat_session = model.start_chat(history=chat_history)
            response = chat_session.send_message(message)
            return response.text
        except Exception as e:
            print(f"Gemini (old SDK) error: {e}")

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
