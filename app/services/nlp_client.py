import logging
import httpx
from app.core.config import settings
from app.models.schemas import NLPResult

logger = logging.getLogger(__name__)

async def translate_and_detect(raw_text: str) -> NLPResult:
    try:
        async with httpx.AsyncClient(timeout=settings.EXTERNAL_API_TIMEOUT) as client:
            resp = await client.post(settings.NLP_API_URL, json={"text": raw_text})
            resp.raise_for_status()
            data = resp.json()
            return NLPResult(
                detected_language=data.get("detected_language", "en"),
                translated_text=data.get("translated_text", raw_text),
            )
    except Exception as exc:
        logger.error("NLP API error: %s", exc)
        return NLPResult(detected_language="en", translated_text=raw_text)
