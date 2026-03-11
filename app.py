"""
EduVora - AI-Powered Smart Learning Management System
Main Flask Application
"""
import os
import json
import uuid
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, flash
)

# Firebase Admin
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth

# AI Modules
from ai.classifier import classify_level, get_level_info, calculate_topic_scores
from ai.weak_area import detect_weak_areas, get_weak_area_summary, get_improvement_tips
from ai.quiz_generator import generate_quiz, generate_diagnostic_quiz
from ai.recommender import get_recommendations, get_topic_resources, get_level_roadmap
from ai.chatbot import chat

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "eduvora-hackathon-secret-2024")

# ─── Firebase Setup ─────────────────────────────────────────────────────────────
db = None
firebase_initialized = False

try:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        firebase_initialized = True
        print("✅ Firebase initialized successfully")
    else:
        print("⚠️  serviceAccountKey.json not found — running in demo mode")
except Exception as e:
    print(f"⚠️  Firebase init error: {e} — running in demo mode")

# Firebase Web Config for frontend
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY", ""),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
    "appId": os.getenv("FIREBASE_APP_ID", ""),
}


# ─── Helpers ────────────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def get_user_data(user_id: str) -> dict:
    """Fetch user data from Firestore or return demo data."""
    if db and user_id:
        try:
            doc = db.collection("users").document(user_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception:
            pass

    # Demo mode fallback
    return session.get("demo_user", {
        "name": "Demo Student",
        "email": "demo@eduvora.com",
        "level": "Beginner",
        "score": 0,
        "quiz_count": 0,
        "weak_areas": [],
        "topic_scores": {},
        "quiz_history": [],
        "joined": datetime.now().isoformat(),
    })


def save_user_data(user_id: str, data: dict):
    """Save user data to Firestore or session."""
    if db and user_id and user_id != "demo":
        try:
            db.collection("users").document(user_id).set(data, merge=True)
            return
        except Exception as e:
            print(f"Firestore save error: {e}")
    # demo mode — save to session
    session["demo_user"] = data
    session.modified = True


# ─── Auth Routes ────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        id_token = data.get("idToken")
        name = data.get("name", "Student")
        email = data.get("email", "")
        uid = data.get("uid", "")

        if firebase_initialized and id_token:
            try:
                decoded = firebase_auth.verify_id_token(id_token)
                uid = decoded["uid"]
                email = decoded.get("email", email)
                name = decoded.get("name", name)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        if not uid:
            # Demo mode login
            uid = "demo"
            name = data.get("name", "Demo Student")
            email = data.get("email", "demo@eduvora.com")

        session["user_id"] = uid
        session["user_name"] = name
        session["user_email"] = email

        # Check if user exists
        user_data = get_user_data(uid)
        if not user_data.get("level"):
            # New user — init profile
            user_data = {
                "name": name,
                "email": email,
                "level": None,
                "score": 0,
                "quiz_count": 0,
                "weak_areas": [],
                "topic_scores": {},
                "quiz_history": [],
                "joined": datetime.now().isoformat(),
            }
            save_user_data(uid, user_data)
            if request.is_json:
                return jsonify({"redirect": url_for("quiz", topic="diagnostic")})
            return redirect(url_for("quiz", topic="diagnostic"))

        if request.is_json:
            return jsonify({"redirect": url_for("dashboard")})
        return redirect(url_for("dashboard"))

    return render_template("login.html", firebase_config=FIREBASE_CONFIG)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        id_token = data.get("idToken")
        name = data.get("name", "Student")
        email = data.get("email", "")
        uid = data.get("uid", f"demo_{uuid.uuid4().hex[:8]}")

        if firebase_initialized and id_token:
            try:
                decoded = firebase_auth.verify_id_token(id_token)
                uid = decoded["uid"]
                email = decoded.get("email", email)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        session["user_id"] = uid
        session["user_name"] = name
        session["user_email"] = email

        user_data = {
            "name": name,
            "email": email,
            "level": None,
            "score": 0,
            "quiz_count": 0,
            "weak_areas": [],
            "topic_scores": {},
            "quiz_history": [],
            "joined": datetime.now().isoformat(),
        }
        save_user_data(uid, user_data)

        if request.is_json:
            return jsonify({"redirect": url_for("quiz", topic="diagnostic")})
        return redirect(url_for("quiz", topic="diagnostic"))

    return render_template("register.html", firebase_config=FIREBASE_CONFIG)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# Demo login for hackathon judges / testing
@app.route("/demo-login")
def demo_login():
    uid = "demo"
    session["user_id"] = uid
    session["user_name"] = "Demo Student"
    session["user_email"] = "demo@eduvora.com"
    session["demo_user"] = {
        "name": "Demo Student",
        "email": "demo@eduvora.com",
        "level": "Intermediate",
        "score": 55,
        "quiz_count": 3,
        "weak_areas": ["Probability & Statistics", "Linear Algebra"],
        "topic_scores": {
            "Machine Learning Basics": 80,
            "Linear Regression": 65,
            "Classification": 60,
            "Probability & Statistics": 35,
            "Linear Algebra": 30,
            "Data Preprocessing": 70,
            "Overfitting & Underfitting": 55,
            "Neural Networks": 40,
        },
        "quiz_history": [
            {"date": "2024-03-10", "score": 40, "level": "Beginner", "topic": "diagnostic"},
            {"date": "2024-03-11", "score": 55, "level": "Intermediate", "topic": "Machine Learning Basics"},
            {"date": "2024-03-11", "score": 65, "level": "Intermediate", "topic": "Linear Regression"},
        ],
        "joined": "2024-03-10T09:00:00",
    }
    return redirect(url_for("dashboard"))


# ─── Dashboard ─────────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    level = user_data.get("level") or "Beginner"

    if not user_data.get("level"):
        return redirect(url_for("quiz", topic="diagnostic"))

    level_info = get_level_info(level)
    weak_areas = user_data.get("weak_areas", [])
    topic_scores = user_data.get("topic_scores", {})
    tips = get_improvement_tips(weak_areas[:3])
    recommendations = get_recommendations(level, weak_areas, limit=4)
    roadmap = get_level_roadmap(level)
    quiz_history = user_data.get("quiz_history", [])

    return render_template(
        "dashboard.html",
        user=user_data,
        level=level,
        level_info=level_info,
        weak_areas=weak_areas,
        topic_scores=json.dumps(topic_scores),
        topic_scores_raw=topic_scores,
        tips=tips,
        recommendations=recommendations,
        roadmap=roadmap,
        quiz_history=quiz_history[-5:],
        score=user_data.get("score", 0),
    )


# ─── Quiz Routes ───────────────────────────────────────────────────────────────
@app.route("/quiz/<topic>")
@login_required
def quiz(topic):
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    level = user_data.get("level") or "Beginner"
    weak_areas = user_data.get("weak_areas", [])

    if topic == "diagnostic":
        questions = generate_diagnostic_quiz()
        title = "Diagnostic Quiz — Let's find your level!"
        subtitle = "Answer honestly. This helps us personalize your learning path."
    else:
        # 'personalized' and 'all' mean no specific topic filter
        topic_filter = topic if topic not in ("all", "personalized") else None
        use_weak = topic == "personalized"

        questions = generate_quiz(
            topic=topic_filter,
            level=level,
            weak_areas=weak_areas if use_weak else None,
        )

        # Fallback: if no questions generated, use diagnostic quiz
        if not questions:
            questions = generate_diagnostic_quiz()

        if topic == "personalized":
            title = "Personalized Quiz"
            subtitle = f"AI-tuned to your {level} level and weak areas"
        elif topic == "all":
            title = "Full Practice Quiz"
            subtitle = f"Covering all topics at {level} difficulty"
        else:
            title = f"Quiz: {topic}"
            subtitle = f"Difficulty tuned for {level} level"


    # Store questions in session for validation
    session["current_quiz"] = {
        "topic": topic,
        "questions": questions,
        "start_time": datetime.now().isoformat(),
    }

    return render_template(
        "quiz.html",
        questions=questions,
        topic=topic,
        title=title,
        subtitle=subtitle,
        level=level,
        questions_json=json.dumps(questions),
    )


@app.route("/quiz/submit", methods=["POST"])
@login_required
def submit_quiz():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    current_quiz = session.get("current_quiz", {})

    data = request.get_json(silent=True) or request.form
    answers = data.get("answers", [])
    time_taken = int(data.get("time_taken", 0))  # seconds

    if isinstance(answers, str):
        try:
            answers = json.loads(answers)
        except Exception:
            answers = []

    questions = current_quiz.get("questions", [])
    topic = current_quiz.get("topic", "general")

    if not questions:
        return redirect(url_for("dashboard"))

    # Calculate score
    correct = 0
    answer_details = []
    for i, q in enumerate(questions):
        user_ans = answers[i] if i < len(answers) else -1
        is_correct = (user_ans == q["correct_answer"])
        if is_correct:
            correct += 1
        answer_details.append({
            "question": q["question"],
            "user_answer": user_ans,
            "correct_answer": q["correct_answer"],
            "correct_option": q["options"][q["correct_answer"]],
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
        })

    score_pct = round((correct / len(questions)) * 100) if questions else 0
    avg_time = round(time_taken / len(questions)) if questions else 0

    # AI Classification
    new_level = classify_level(score_pct, avg_time)
    topic_scores = calculate_topic_scores(answers, questions)

    # Update cumulative topic scores
    existing_topic_scores = user_data.get("topic_scores", {})
    for t, s in topic_scores.items():
        if t in existing_topic_scores:
            # Weighted average (70% new, 30% old)
            existing_topic_scores[t] = round(0.3 * existing_topic_scores[t] + 0.7 * s, 1)
        else:
            existing_topic_scores[t] = s

    # Detect weak areas
    weak_summary = get_weak_area_summary(existing_topic_scores)
    weak_areas = [item["topic"] for item in weak_summary["weak"]]

    # Update user data
    quiz_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "score": score_pct,
        "level": new_level,
        "topic": topic,
        "correct": correct,
        "total": len(questions),
    }
    history = user_data.get("quiz_history", [])
    history.append(quiz_entry)

    updated_data = {
        **user_data,
        "level": new_level,
        "score": score_pct,
        "quiz_count": user_data.get("quiz_count", 0) + 1,
        "weak_areas": weak_areas,
        "topic_scores": existing_topic_scores,
        "quiz_history": history,
    }
    save_user_data(user_id, updated_data)

    # Store results in session
    session["last_result"] = {
        "score": score_pct,
        "correct": correct,
        "total": len(questions),
        "new_level": new_level,
        "topic": topic,
        "answer_details": answer_details,
        "weak_areas": weak_areas,
        "topic_scores": topic_scores,
        "weak_summary": weak_summary,
        "time_taken": time_taken,
    }

    return jsonify({"redirect": url_for("results")})


@app.route("/results")
@login_required
def results():
    result = session.get("last_result")
    if not result:
        return redirect(url_for("dashboard"))

    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    level = result.get("new_level", "Beginner")
    level_info = get_level_info(level)
    weak_areas = result.get("weak_areas", [])
    recommendations = get_recommendations(level, weak_areas, limit=6)
    tips = get_improvement_tips(weak_areas[:3])

    return render_template(
        "results.html",
        result=result,
        level_info=level_info,
        recommendations=recommendations,
        tips=tips,
        topic_scores=json.dumps(result.get("topic_scores", {})),
        user=user_data,
    )


# ─── Recommendations ───────────────────────────────────────────────────────────
@app.route("/recommendations")
@login_required
def recommendations():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    level = user_data.get("level", "Beginner")
    weak_areas = user_data.get("weak_areas", [])

    recs = get_recommendations(level, weak_areas, limit=12)
    roadmap = get_level_roadmap(level)
    tips = get_improvement_tips(weak_areas)
    level_info = get_level_info(level)

    return render_template(
        "recommendations.html",
        recommendations=recs,
        roadmap=roadmap,
        tips=tips,
        weak_areas=weak_areas,
        level=level,
        level_info=level_info,
        user=user_data,
    )


# ─── Progress ──────────────────────────────────────────────────────────────────
@app.route("/progress")
@login_required
def progress():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    level = user_data.get("level", "Beginner")
    topic_scores = user_data.get("topic_scores", {})
    quiz_history = user_data.get("quiz_history", [])
    weak_summary = get_weak_area_summary(topic_scores)
    level_info = get_level_info(level)

    # Build chart data
    score_trend = [{"date": q["date"], "score": q["score"]} for q in quiz_history]

    return render_template(
        "progress.html",
        user=user_data,
        level=level,
        level_info=level_info,
        topic_scores=json.dumps(topic_scores),
        topic_scores_raw=topic_scores,
        quiz_history=quiz_history,
        score_trend=json.dumps(score_trend),
        weak_summary=weak_summary,
        total_quizzes=len(quiz_history),
        avg_score=round(
            sum(q["score"] for q in quiz_history) / len(quiz_history), 1
        ) if quiz_history else 0,
    )


# ─── Chatbot ───────────────────────────────────────────────────────────────────
@app.route("/chatbot")
@login_required
def chatbot():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    return render_template("chatbot.html", user=user_data)


@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Empty message"}), 400

    if len(message) > 1000:
        return jsonify({"error": "Message too long"}), 400

    try:
        response = chat(message, history)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── API Endpoints ─────────────────────────────────────────────────────────────
@app.route("/api/user-stats")
@login_required
def api_user_stats():
    user_id = session["user_id"]
    user_data = get_user_data(user_id)
    return jsonify({
        "level": user_data.get("level", "Beginner"),
        "score": user_data.get("score", 0),
        "quiz_count": user_data.get("quiz_count", 0),
        "weak_areas": user_data.get("weak_areas", []),
    })


# ─── Error Handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("login.html", firebase_config=FIREBASE_CONFIG), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("🎓 EduVora AI-LMS starting...")
    print(f"   Firebase: {'✅ Connected' if firebase_initialized else '⚠️  Demo Mode'}")
    print("   Visit: http://localhost:5001")
    app.run(debug=True, port=5001)
