import logging
import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat
from app.core.config import settings

# Configure logging to show DEBUG and INFO messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Set specific loggers
logging.getLogger("app").setLevel(logging.DEBUG)
logging.getLogger("app.services").setLevel(logging.DEBUG)
logging.getLogger("app.api").setLevel(logging.DEBUG)

# Create app logger
app_logger = logging.getLogger("app")

app = FastAPI(title="Taxi Support Chatbot API", version="1.0.0")

# Log startup
@app.on_event("startup")
def startup_event():
    app_logger.info("=" * 80)
    app_logger.info("CHATBOT API STARTUP - LOGGING CONFIGURED")
    app_logger.info("=" * 80)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "taxi-support-chatbot"}
