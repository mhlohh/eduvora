from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduVora API"
    secret_key: str = "change-this-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+psycopg2://eduvora:eduvora@db:5432/eduvora"
    google_client_id: str = ""
    allow_insecure_google_fallback: bool = True
    firebase_credentials_path: str = "serviceAccountKey.json"
    code_runner_url: str = "http://code-runner:8001"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    tutor_temperature: float = 0.4
    tutor_max_tokens: int = 500

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
