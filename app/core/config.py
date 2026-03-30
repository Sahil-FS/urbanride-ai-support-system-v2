from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EXTERNAL_API_TIMEOUT: int = 5
    CONFIDENCE_THRESHOLD: float = 0.55
    DEFAULT_LANGUAGE: str = "en"
    INTENT_API_URL: str = "http://localhost:8001/detect"
    NLP_API_URL: str = "http://localhost:8002/translate"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
