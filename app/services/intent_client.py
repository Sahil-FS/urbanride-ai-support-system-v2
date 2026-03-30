import logging
from app.models.schemas import IntentResult
from .intent_service.service import detect_intent as local_detect

logger = logging.getLogger(__name__)

async def detect_intent(text: str) -> IntentResult:
    try:
        # Calling local ML model instead of external API
        intent, confidence = local_detect(text)
        return IntentResult(
            intent=intent,
            confidence=float(confidence),
        )
    except Exception as exc:
        logger.error("Local Intent Service error: %s", exc)
        return IntentResult(intent="unknown_intent", confidence=0.0)
