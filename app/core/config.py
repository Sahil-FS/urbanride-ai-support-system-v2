from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CONFIDENCE_THRESHOLD: float = 0.25
    DEFAULT_LANGUAGE: str = "en"
    MODEL_ROOT: str = "models"
    INTENT_MODEL_DIR: str = "models/intent"
    NLP_MODEL_DIR: str = "models/nlp"
    SHARED_MODEL_DIR: str = "models/shared"

    class Config:
        env_file = ".env"

settings = Settings()
