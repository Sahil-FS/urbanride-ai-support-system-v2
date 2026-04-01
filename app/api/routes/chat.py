import logging
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.nlp_client import translate_and_detect
from app.services.intent_client import detect_intent
from app.services.chatbot_engine import get_response, is_call_trigger

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    raw_message   = request.message.strip()
    original_text = (request.original_text or raw_message).strip()

    # ── Direct call trigger ───────────────────────────────────────────────────
    # User clicked "Call Support Now" pill or typed equivalent
    if is_call_trigger(raw_message) or is_call_trigger(original_text):
        return ChatResponse(
            intent="contact_support",
            response=(
                "Connecting you to our support team now. "
                "Please tap the button below to call us directly. "
                "Our team is available 24/7."
            ),
            confidence=1.0,
            sub_options=[],
            show_call_button=True,
        )

    # ── Normal pipeline: NLP → Intent Detection → Decision Tree ──────────────
    try:
        nlp_result    = await translate_and_detect(raw_message)
        intent_result = await detect_intent(nlp_result.translated_text)
    except Exception as e:
        logger.error("Pipeline error: %s", e)
        return ChatResponse(
            intent="fallback",
            response=(
                "I was not able to understand your request clearly. "
                "Please try rephrasing, or connect with a live agent."
            ),
            confidence=0.0,
            sub_options=["Call Support Now"],
            show_call_button=True,
        )

    # ── get_response now receives original_text ───────────────────────────────
    # This activates PILL_INTENT_MAP in chatbot_engine.py
    # which maps pill labels directly to specific intents — kills all loops
    result = get_response(
        intent=intent_result.intent,
        confidence=intent_result.confidence,
        original_text=original_text,
    )

    logger.info(
        "msg=%r | original=%r | intent=%s | resolved=%s | conf=%.2f",
        raw_message,
        original_text,
        intent_result.intent,
        result["resolved_intent"],
        intent_result.confidence,
    )

    return ChatResponse(
        intent=result["resolved_intent"],
        response=result["response"],
        confidence=round(intent_result.confidence, 4),
        sub_options=result["sub_options"],
        show_call_button=result["show_call_button"],
    )