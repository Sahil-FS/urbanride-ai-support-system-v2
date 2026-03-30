from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, admin_ticket
from app.core.config import settings
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(title="Taxi Support Chatbot API", version="1.0.0")

from app.models.support_ticket import Base as TicketBase
from sqlalchemy import create_engine
engine = create_engine("sqlite:///./chatbot_support.db")
TicketBase.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(admin_ticket.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "taxi-support-chatbot"}
