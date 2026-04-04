import logging
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.intent_client import detect_intent
from app.services.chatbot_engine import get_response, is_call_trigger
from app.services.translation_service import (
    localize_intent_response,
    normalize_user_message,
    translate_sub_options,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    raw_message   = request.message.strip()
    original_text = (request.original_text or raw_message).strip()
    requested_language = (request.language or "en").lower()
    language = requested_language if requested_language in {"en", "mr", "hi"} else "en"
    normalized_raw_message = normalize_user_message(raw_message)
    normalized_original_text = normalize_user_message(original_text)

    logger.info("=" * 80)
    logger.info("CHAT REQUEST RECEIVED")
    logger.info(f"  raw_message: {raw_message!r}")
    logger.info(f"  original_text: {original_text!r}")
    logger.info(f"  language: {language}")
    logger.info(f"  normalized_raw: {normalized_raw_message!r}")
    logger.info(f"  normalized_orig: {normalized_original_text!r}")

    # ── Direct call trigger ───────────────────────────────────────────────────
    # User clicked "Call Support Now" pill or typed equivalent
    if is_call_trigger(normalized_raw_message) or is_call_trigger(normalized_original_text):
        logger.info(">>> CALL TRIGGER DETECTED")
        response_text = localize_intent_response(
            "contact_support",
            "Connecting you to our support team now. "
            "Please tap the button below to call us directly. "
            "Our team is available 24/7.",
            language,
        )
        return ChatResponse(
            intent="contact_support",
            response=response_text,
            confidence=1.0,
            sub_options=[],
            show_call_button=True,
            language=language,
        )

    # ── Internal pipeline: Raw input → Intent Detection → Decision Tree ──────
    try:
        logger.info(">>> INTENT DETECTION STARTING")
        intent_result = await detect_intent(normalized_raw_message)
        logger.info(f"    intent_result: intent={intent_result.intent!r}, conf={intent_result.confidence:.4f}")
    except Exception as e:
        logger.error("Pipeline error: %s", e)
        fallback_response = (
            "I was not able to understand your request clearly. "
            "Please try rephrasing, or connect with a live agent."
        )
        return ChatResponse(
            intent="fallback",
            response=localize_intent_response("fallback", fallback_response, language),
            confidence=0.0,
            sub_options=translate_sub_options(["Call Support Now"], language),
            show_call_button=True,
            language=language,
        )

    # ── get_response now receives original_text ───────────────────────────────
    # This activates PILL_INTENT_MAP in chatbot_engine.py
    # which maps pill labels directly to specific intents — kills all loops
    logger.info(">>> CHATBOT ENGINE DECISION TREE")
    logger.info(f"    input: intent={intent_result.intent!r}, original_text={normalized_original_text!r}")
    result = get_response(
        intent=intent_result.intent,
        confidence=intent_result.confidence,
        original_text=normalized_original_text,
    )
    logger.info(f"    resolved_intent: {result['resolved_intent']!r}")
    logger.info(f"    sub_options: {result['sub_options']}")
    logger.info(f"    show_call_button: {result['show_call_button']}")

    logger.info(
        "msg=%r | original=%r | intent=%s | resolved=%s | conf=%.2f | lang=%s",
        raw_message,
        original_text,
        intent_result.intent,
        result["resolved_intent"],
        intent_result.confidence,
        language,
    )

    # ── Translate response if target language is not English ──────────────────
    localized_response = localize_intent_response(
        result["resolved_intent"],
        result["response"],
        language,
    )
    localized_sub_options = translate_sub_options(result["sub_options"], language)

    logger.info(f">>> LOCALIZATION")
    logger.info(f"    language: {language}")
    logger.info(f"    response_en: {result['response']!r}")
    logger.info(f"    response_localized: {localized_response!r}")
    logger.info(f"    sub_options_orig: {result['sub_options']}")
    logger.info(f"    sub_options_localized: {localized_sub_options}")
    logger.info("=" * 80)

    return ChatResponse(
        intent=result["resolved_intent"],
        response=localized_response,
        confidence=round(intent_result.confidence, 4),
        sub_options=localized_sub_options,
        show_call_button=result["show_call_button"],
        language=language,
    )