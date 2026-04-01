from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INTENT_API_URL: str = "http://localhost:8001/detect"
    NLP_API_URL: str = "http://localhost:8002/translate"
    EXTERNAL_API_TIMEOUT: int = 5
    CONFIDENCE_THRESHOLD: float = 0.55
    DEFAULT_LANGUAGE: str = "en"
    MODEL_ROOT: str = "models"
    INTENT_MODEL_DIR: str = "models/intent"
    NLP_MODEL_DIR: str = "models/nlp"
    SHARED_MODEL_DIR: str = "models/shared"

    class Config:
        env_file = ".env"

settings = Settings()
