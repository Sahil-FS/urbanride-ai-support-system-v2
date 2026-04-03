import logging
import re
from app.models.schemas import IntentResult
from app.services.intent_model import get_intent_model

logger = logging.getLogger(__name__)


def _preprocess_for_intent(text: str) -> str:
    """Normalize user text before feeding the local multilingual model."""
    if not text:
        return ""
    # Keep multilingual characters intact, only normalize spacing/control chars.
    cleaned = text.replace("\n", " ").replace("\t", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


async def detect_intent(text: str) -> IntentResult:
    """
    Detect intent using local multilingual model loaded from models/intent.
    """
    try:
        model = get_intent_model()
        prepared_text = _preprocess_for_intent(text)
        logger.info(f"[INTENT] Input text: {text!r}")
        logger.info(f"[INTENT] Prepared text: {prepared_text!r}")
        result = model.predict(prepared_text)
        logger.info(
            "[INTENT] Model prediction: %s (confidence: %.4f)",
            result.intent,
            result.confidence,
        )
        return result
    except Exception as exc:
        logger.error("Intent detection error: %s", exc)
        return IntentResult(intent="unknown_intent", confidence=0.0)
