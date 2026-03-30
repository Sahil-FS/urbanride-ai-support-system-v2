from .intent_detection import predict

def detect_intent(text: str) -> tuple[str, float]:
    """
    Wrapper for the ML model's predict function.
    Returns: (intent, confidence)
    """
    result = predict(text)
    return result.intent, result.confidence
