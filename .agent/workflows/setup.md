---
description: common development and deployment tasks for EduVora
---

# Development Workflow

## Running the App Locally

1. **Start the Flask Server**
   // turbo
   `python app.py`
   *Default port: 5001*

2. **Run with Docker (Recommended)**
   // turbo
   `docker-compose up --build`
   *Builds the full stack including DB, Backend, and Frontend*

## Handling Secrets

1. **Update API Keys**
   - Edit the `.env` file in the root directory.
   - For Firestore, ensure `serviceAccountKey.json` is present in the root.

2. **GitHub Push Protection**
   - If a push is blocked due to secrets, run:
   `git reset HEAD~1`
   - Scrub secrets from `.env.example` before re-committing.

## Deployment to Render

1. **Prepare Secrets**
   - Copy `.env` content to Render's "Environment Variables" dashboard.
   - Add `serviceAccountKey.json` as a "Secret File" in the Render web service settings.

2. **Deploy**
   - Push to `main` branch.
   - Render will build using the Dockerfiles in `backend/` and `frontend/`.
