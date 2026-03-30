import json
import os

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "multilingual_data.json"), encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

with open(os.path.join(BASE_DIR, "responses.json"), encoding="utf-8") as f:
    RESPONSES = json.load(f)

def detect_language_and_intent(text: str):
    # Mapping for frontend pills
    mapping = {
        "track ride": "track_ride",
        "driver issue": "driver_issue",
        "payment issue": "payment_issue",
        "cancel ride": "cancel_ride",
        "refund request": "refund_request",
        "safety concern": "safety_issue"
    }

    text = text.lower().strip()

    if text in mapping:
        return mapping[text], "en"

    for lang_key in ["hi_to_en", "mr_to_en"]:
        for phrase, intent in TRANSLATIONS.get(lang_key, {}).items():
            if phrase in text:
                lang = "hi" if "hi" in lang_key else "mr"
                return intent, lang

    return None, "en"

def get_response(intent: str, lang: str):
    return RESPONSES.get(lang, {}).get("responses", {}).get(
        intent,
        RESPONSES.get(lang, {}).get("responses", {}).get("fallback", "Sorry")
    )
