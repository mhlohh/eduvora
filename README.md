# EduVora - AI Powered Adaptive Learning Platform

## Stack
- Frontend: Next.js + React + TailwindCSS + Chart.js + Monaco
- Backend: FastAPI
- Database: PostgreSQL
- Auth: JWT + Google login endpoint
- Optional Firebase login endpoint
- AI Layer: `ai_engine/`
- Code Execution: Dockerized sandbox service (`code-runner`)

## Run with Docker
```bash
docker compose up --build
```

## URLs
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Code runner: http://localhost:8001/health

## Key Flows Implemented
1. Notification permission screen
2. Login (mobile/email/google)
3. Personalization
4. Course selection
5. Diagnostic adaptive quiz (10 questions, skip limit = 2)
6. AI learner profile generation
7. Personalized recommendations
8. Dashboard with charts
9. AI tutor Q&A
10. Coding workspace + sandbox code run + error tracking

## Auth Endpoints
- `POST /api/auth/login` (email/mobile + password)
- `POST /api/auth/google` (Google ID token verification; supports strict mode with `GOOGLE_CLIENT_ID`)
- `POST /api/auth/firebase` (Firebase ID token verification if `serviceAccountKey.json` is available)

## Generative AI Tutor
- Endpoint: `POST /api/chat`
- Uses learner profile context (`knowledge_level`, `learning_speed`, weak/strong topics) for personalized responses.
- Powered by **local Ollama** running the **DeepSeek R1** model.
- If Ollama is running and `deepseek-r1` is available, the tutor uses full generative reasoning.
- Falls back to rule-based responses if the local LLM service is unavailable.

## Setup & Configuration

### 1. Environment Variables
Copy `.env.example` to `.env` and configure the following:
```bash
# Ollama AI Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1
```

### 2. Ollama Setup
1. [Install Ollama](https://ollama.com/download)
2. Pull the required model:
   ```bash
   ollama pull deepseek-r1
   ```

### 3. Installation
```bash
pip install -r requirements.txt
python app.py
```
