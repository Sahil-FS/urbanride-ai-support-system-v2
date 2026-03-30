from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    original_text: str = ""
    user_id: int = 1


class ChatResponse(BaseModel):
    message: str
    next_options: List[dict] = []
    actions: List[dict] = []
    show_feedback: bool = False
    escalate: bool = False
    ticket_ref: str | None = None


class IntentResult(BaseModel):
    intent: str
    confidence: float


class NLPResult(BaseModel):
    detected_language: str
    translated_text: str