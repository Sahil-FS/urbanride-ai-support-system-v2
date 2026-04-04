from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    original_text: str = ""
    language: str = Field(default="en", description="Language code: 'en', 'mr', or 'hi'")


class ChatResponse(BaseModel):
    intent: str
    response: str
    confidence: float
    sub_options: List[str] = []
    show_call_button: bool = False
    language: str = "en"


class IntentResult(BaseModel):
    intent: str
    confidence: float