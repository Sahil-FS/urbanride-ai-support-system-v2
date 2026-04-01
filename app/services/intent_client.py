import logging
from app.models.schemas import IntentResult
from app.services.intent_model import get_intent_model

logger = logging.getLogger(__name__)

async def detect_intent(text: str) -> IntentResult:
    """
    Detect intent using local DistilBERT model loaded from models/intent
    """
    try:
        model = get_intent_model()
        result = model.predict(text)
        logger.info(f"Intent detected: {result.intent} (confidence: {result.confidence:.4f})")
        return result
    except Exception as exc:
        logger.error("Intent detection error: %s", exc)
        return IntentResult(intent="unknown_intent", confidence=0.0)
