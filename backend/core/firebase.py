import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from backend.core.config import settings


firebase_ready = False


def init_firebase() -> bool:
    global firebase_ready
    if firebase_ready:
        return True

    cred_path = settings.firebase_credentials_path
    if not os.path.exists(cred_path):
        return False

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        firebase_ready = True
        return True
    except Exception:
        firebase_ready = False
        return False


def verify_firebase_token(id_token: str):
    if not init_firebase():
        return None
    try:
        return firebase_auth.verify_id_token(id_token)
    except Exception:
        return None
