import logging
from datetime import datetime
import json

# Setup a dedicated logger for telemetry
logger = logging.getLogger("telemetry")

def log_event(
    intent: str,
    confidence: float,
    latency: float,
    status: str = "success",
    error: str = None
):
    """
    Structured telemetry logging for intent classification events.
    Captures intent, confidence, latency, and outcome status.
    """
    event_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "intent": intent,
        "confidence": round(confidence, 4),
        "latency": round(latency, 4),
        "status": status,
        "error": error
    }
    # Log as a JSON string for easier downstream parsing (ELK/Splunk/CloudWatch)
    logger.info(json.dumps(event_data))
