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
- Endpoint: `POST /api/tutor/chat`
- Uses learner profile context (`knowledge_level`, `learning_speed`, weak/strong topics) for personalized responses.
- If `OPENAI_API_KEY` is configured, tutor runs in LLM mode using chat completions.
- If no key is configured or provider fails, it automatically falls back to rule-based responses.
