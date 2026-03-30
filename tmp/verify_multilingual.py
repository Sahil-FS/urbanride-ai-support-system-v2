import sys
import os
import io

# Set encoding for Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.services.multilingual_service import detect_language_and_intent, get_response

def test_cases():
    tests = [
        {
            "name": "Hindi - Track Ride",
            "text": "ड्राइवर कहाँ है",
            "expected_intent": "track_ride",
            "expected_lang": "hi"
        },
        {
            "name": "Marathi - Cancel Ride",
            "text": "राईड रद्द करा",
            "expected_intent": "cancel_ride",
            "expected_lang": "mr"
        },
        {
            "name": "English - Track Ride (ML fallback)",
            "text": "Track my ride",
            "expected_intent": None, # Should return None to trigger ML fallback
            "expected_lang": "en"
        }
    ]

    for test in tests:
        intent, lang = detect_language_and_intent(test["text"])
        print(f"CASE: {test['name']}")
        print(f"  Input: {test['text']}")
        print(f"  Detected Intent: {intent} (Expected: {test['expected_intent']})")
        print(f"  Detected Lang: {lang} (Expected: {test['expected_lang']})")
        
        actual_intent = intent if intent else "track_ride" # Mocking ML result for English track ride
        response = get_response(actual_intent, lang)
        print(f"  Response: {response}")
        print("-" * 20)

if __name__ == "__main__":
    test_cases()
