from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    original_text: str = ""


class ChatResponse(BaseModel):
    intent: str
    response: str
    confidence: float
    sub_options: List[str] = []
    show_call_button: bool = False


class IntentResult(BaseModel):
    intent: str
    confidence: float


class NLPResult(BaseModel):
    detected_language: str
    translated_text: str