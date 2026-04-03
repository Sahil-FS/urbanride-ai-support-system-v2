"""
translation_service.py — Deterministic multilingual helpers
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


# Canonical English labels used by the decision tree.
EN_TO_MR_LABEL_MAP: dict[str, str] = {
    "Track Ride": "राइड ट्रॅक करा",
    "Driver Issue": "ड्राइव्हर समस्या",
    "Payment Issue": "पेमेंट समस्या",
    "Cancel Ride": "राइड रद्द करा",
    "Refund Request": "रिफंड विनंती",
    "Safety Concern": "सुरक्षा चिंता",
    "Talk to Support": "सपोर्टशी बोला",
    "Driver Not Arrived": "ड्रायव्हर पोहोचला नाही",
    "Driver is Late": "ड्रायव्हर उशिरा आहे",
    "Cannot Contact Driver": "ड्रायव्हरशी संपर्क होत नाही",
    "Contact Driver": "ड्रायव्हरशी संपर्क करा",
    "Cancel Ride for Free": "राइड मोफत रद्द करा",
    "Call Support Now": "ग्राहक सपोर्टला कॉल करा",
    "Report Issue": "समस्या नोंदवा",
    "Update Pickup Pin": "पिकअप पिन अपडेट करा",
    "Ask Driver to Start": "ड्रायव्हरला राइड सुरू करायला सांगा",
    "Cancel My Current Ride": "माझी चालू राइड रद्द करा",
    "Driver Cancelled on Me": "ड्रायव्हरने माझी राइड रद्द केली",
    "Cancellation Fee Issue": "रद्द शुल्काबद्दल समस्या",
    "Dispute the Fee": "शुल्कावर हरकती नोंदवा",
    "Payment Failed": "पेमेंट अयशस्वी झाले",
    "I Was Charged Twice": "माझ्याकडून दोनदा शुल्क घेतले गेले",
    "Wrong Fare Charged": "चुकीचे भाडे आकारले गेले",
    "Change Payment Method": "पेमेंट पद्धत बदला",
    "Dispute the Fare": "भाड्यावर हरकती नोंदवा",
    "Dispute the Charge": "शुल्कावर हरकती नोंदवा",
    "Check Refund Status": "रिफंड स्थिती तपासा",
    "Refund Not Received": "रिफंड मिळाला नाही",
    "Request a New Refund": "नवीन रिफंडची विनंती करा",
    "Escalate My Refund": "माझा रिफंड एस्कलेट करा",
    "Driver Misbehavior": "ड्रायव्हरचे गैरवर्तन",
    "Rash Driving": "बेदरकार ड्रायव्हिंग",
    "SOS Emergency": "SOS आपत्कालीन मदत",
    "Accident Report": "अपघाताची नोंद करा",
    "Report This Driver": "या ड्रायव्हरची तक्रार करा",
    "Contact My Driver": "माझ्या ड्रायव्हरशी संपर्क करा",
    "Report Lost Item": "हरवलेल्या वस्तूची नोंद करा",
    "Login Problem": "लॉगिन समस्या",
    "Update My Profile": "माझे प्रोफाइल अपडेट करा",
    "Retry the Coupon": "कूपन पुन्हा वापरून पाहा",
    "Driver Took Long Route": "ड्रायव्हरने लांब मार्ग घेतला",
    "Dispute the Route": "मार्गावर हरकती नोंदवा",
}

# Allow quick replies with emoji to map cleanly as well.
EN_TO_MR_LABEL_MAP.update(
    {
        "🚕 Track Ride": "🚕 राइड ट्रॅक करा",
        "👤 Driver Issue": "👤 ड्राइव्हर समस्या",
        "💳 Payment Issue": "💳 पेमेंट समस्या",
        "❌ Cancel Ride": "❌ राइड रद्द करा",
        "💰 Refund Request": "💰 रिफंड विनंती",
        "🆘 Safety Concern": "🆘 सुरक्षा चिंता",
        "📞 Talk to Support": "📞 सपोर्टसह बोला",
    }
)

MR_TO_EN_LABEL_MAP: dict[str, str] = {v.lower(): k for k, v in EN_TO_MR_LABEL_MAP.items()}

QUICK_REPLY_ICON_PREFIXES = "🚕👤💳❌💰🆘📞"


def _strip_quick_reply_icon(text: str) -> str:
    stripped = text.strip()
    if stripped and stripped[0] in QUICK_REPLY_ICON_PREFIXES:
        return stripped[1:].strip()
    return stripped


# Canonicalize English labels to icon-free forms so pill maps match reliably.
EN_CANONICAL_LABEL_MAP: dict[str, str] = {}
for label in EN_TO_MR_LABEL_MAP.keys():
    EN_CANONICAL_LABEL_MAP[label.lower()] = _strip_quick_reply_icon(label)


MR_INTENT_RESPONSE_MAP: dict[str, str] = {
    "greeting": "नमस्कार! 👋 अर्बन टॅक्सी सपोर्टमध्ये आपले स्वागत आहे. मी आज तुम्हाला कशी मदत करू शकतो?",
    "thank_you": "आपले स्वागत आहे! अजून काही मदत हवी आहे का?",
    "help_request": "मी मदतीसाठी आहे. तुम्ही राइड ट्रॅकिंग, पेमेंट, ड्रायव्हर समस्या, हरवलेल्या वस्तू किंवा अकाउंट मदतीबद्दल विचारू शकता.",
    "track_ride": "मी तुमच्या राइड स्टेटसबद्दल मदत करू शकतो. ड्रायव्हरबाबत नेमकी कोणती समस्या आहे?",
    "driver_not_arrived": "माफ करा, तुमचा ड्रायव्हर अजून पोहोचलेला नाही. कृपया अॅपमधील लाईव्ह मॅप तपासा.",
    "driver_late": "विलंबाबद्दल आम्हाला खेद आहे. तुमचा ड्रायव्हर मार्गात आहे. कृपया लाईव्ह मॅप तपासा.",
    "cannot_contact_driver": "अॅपच्या राइड स्क्रीनमधून ड्रायव्हरला कॉल करून पहा. प्रतिसाद न मिळाल्यास खालील पर्याय निवडा.",
    "wrong_pickup_location": "कृपया अॅप चॅटद्वारे ड्रायव्हरशी पिकअप लोकेशन कन्फर्म करा. तुम्ही पिकअप पिन अपडेटही करू शकता.",
    "ride_not_started": "ड्रायव्हर उपस्थित आहे पण राइड सुरू झाली नसेल तर ड्रायव्हरला अॅपमधून राइड सुरू करायला सांगा.",
    "cancel_ride": "मी राइड रद्द करण्यास मदत करू शकतो. नेमकी परिस्थिती काय आहे?",
    "cancel_ride_now": "तुमची राइड रद्द करण्याची विनंती सबमिट झाली आहे. लागू असल्यास शुल्क ट्रिप हिस्टरीमध्ये दिसेल.",
    "cancel_ride_free": "ड्रायव्हर वेळेत न आल्याने तुम्ही मोफत रद्द करण्यास पात्र आहात. तुमची राइड कोणतेही शुल्क न घेता रद्द झाली आहे.",
    "cancel_by_driver": "ड्रायव्हरने राइड रद्द केल्याबद्दल क्षमस्व. काही मिनिटांत नवीन ड्रायव्हर दिला जाईल.",
    "cancellation_fee_issue": "रद्द शुल्क चुकीने लावले गेले असेल तर आमची टीम 24 तासांत तपासणी करेल.",
    "dispute_fee": "तुमची रद्द शुल्क हरकत नोंदवली आहे. तपासणीनंतर पात्र असल्यास रिफंड केला जाईल.",
    "payment_issue": "मी पेमेंट समस्येत मदत करू शकतो. तुम्हाला कोणती पेमेंट समस्या येत आहे?",
    "payment_failed": "पेमेंट अयशस्वी होण्याचे कारण कार्ड/बॅलन्स समस्या असू शकते. कृपया पेमेंट पद्धत अपडेट करून पुन्हा प्रयत्न करा.",
    "double_payment": "तुमच्याकडून दोनदा शुल्क घेतल्याबद्दल क्षमस्व. हे तातडीने तपासून डुप्लिकेट रक्कम परत केली जाईल.",
    "wrong_fare_charged": "तुमच्याकडून चुकीचे भाडे आकारले गेले असेल तर आम्ही तपासणी करू. तुम्हाला पुढे काय करायचे आहे?",
    "dispute_fare": "तुमची भाडे हरकत यशस्वीपणे नोंदली आहे. पात्र असल्यास फरकाची रक्कम परत केली जाईल.",
    "refund_request": "मी रिफंडबाबत मदत करू शकतो. तुम्हाला काय माहिती हवी आहे?",
    "refund_status": "रिफंड साधारण 5-7 कामकाजाच्या दिवसांत खात्यात दिसतो. 7 दिवसांपेक्षा जास्त झाल्यास एस्कलेट करा.",
    "refund_not_received": "7 दिवसांनंतरही रिफंड न मिळाल्यास आम्ही तो एस्कलेट करू.",
    "refund_initiated": "तुमची रिफंड विनंती यशस्वीरीत्या सुरू झाली आहे. रक्कम 5-7 कामकाजाच्या दिवसांत जमा होईल.",
    "escalate_refund": "तुमचा रिफंड प्रायोरिटी टीमकडे एस्कलेट केला आहे. वरिष्ठ एजंट 4 तासांत तपासणी करेल.",
    "safety_issue": "तुमची सुरक्षा आमच्यासाठी सर्वात महत्त्वाची आहे. कृपया समस्या तपशीलात सांगा.",
    "driver_misbehavior": "ड्रायव्हरचे गैरवर्तन गंभीर आहे. तुमची तक्रार गोपनीय राहील आणि 24 तासांत कारवाई केली जाईल.",
    "rash_driving": "बेदरकार ड्रायव्हिंग गंभीर उल्लंघन आहे. गरज असल्यास तुम्ही सुरक्षित ठिकाणी राइड थांबवू शकता.",
    "accident_report": "कृपया आधी स्वतःची सुरक्षा सुनिश्चित करा. जखमी असल्यास 112 वर त्वरित कॉल करा.",
    "emergency_sos": "🚨 आपत्कालीन स्थिती ओळखली गेली आहे. सक्रिय राइड स्क्रीनमधील SOS बटण ताबडतोब वापरा.",
    "report_driver": "तुमची ड्रायव्हर तक्रार गोपनीय स्वरूपात नोंदली आहे. 24 तासांत कारवाई केली जाईल.",
    "lost_item": "हरवलेली वस्तू मिळवण्यासाठी My Rides मधील संबंधित ट्रिप उघडून Find Lost Item वापरा.",
    "contact_support": "तुम्हाला सपोर्ट टीमशी जोडत आहोत. कृपया खालील बटण वापरून थेट कॉल करा.",
    "login_problem": "लॉगिन स्क्रीनवर Forgot Password वापरून रीसेट करा. समस्या कायम असल्यास सपोर्टशी संपर्क करा.",
    "update_profile": "Profile → Edit Profile मध्ये जाऊन नाव, ईमेल, फोन आणि फोटो अपडेट करू शकता.",
    "route_issue": "मी मार्गाशी संबंधित समस्येत मदत करू शकतो. काय झाले ते सांगा.",
    "long_route_taken": "ड्रायव्हरने अनावश्यक लांब मार्ग घेतल्यास भाड्यावर हरकत नोंदवू शकता. आम्ही GPS डेटा तपासू.",
    "unknown_intent": "तुमची विनंती स्पष्टपणे समजली नाही. कृपया वेगळ्या शब्दांत पुन्हा लिहा किंवा थेट सपोर्टशी संपर्क करा.",
    "fallback": "तुमची विनंती स्पष्टपणे समजली नाही. कृपया वेगळ्या शब्दांत पुन्हा लिहा किंवा थेट सपोर्टशी संपर्क करा.",
}


def normalize_user_message(text: str) -> str:
    """Convert known Marathi/UI labels into canonical English labels for intent routing."""
    if not text:
        return text
    normalized = text.strip()
    normalized_lower = normalized.lower()

    # 1) Marathi/UI label to English canonical label.
    mapped_mr = MR_TO_EN_LABEL_MAP.get(normalized_lower)
    if mapped_mr:
        canonical = _strip_quick_reply_icon(mapped_mr)
        logger.info(f"[NORM] {text!r} -> {canonical!r}")
        return canonical

    # 2) English label (icon or non-icon) to English canonical label.
    mapped_en = EN_CANONICAL_LABEL_MAP.get(normalized_lower)
    if mapped_en:
        logger.info(f"[NORM] {text!r} -> {mapped_en!r}")
        return mapped_en

    # 3) Retry after removing icon prefix from incoming text.
    stripped = _strip_quick_reply_icon(normalized)
    stripped_lower = stripped.lower()
    mapped_mr_stripped = MR_TO_EN_LABEL_MAP.get(stripped_lower)
    if mapped_mr_stripped:
        canonical = _strip_quick_reply_icon(mapped_mr_stripped)
        logger.info(f"[NORM] {text!r} -> {canonical!r}")
        return canonical

    mapped_en_stripped = EN_CANONICAL_LABEL_MAP.get(stripped_lower)
    if mapped_en_stripped:
        logger.info(f"[NORM] {text!r} -> {mapped_en_stripped!r}")
        return mapped_en_stripped

    logger.debug(f"[NORM] {text!r} (no mapping, keeping as-is)")
    return normalized


def localize_intent_response(intent: str, english_response: str, target_language: str) -> str:
    """Return intent-aware localized response text."""
    if target_language == "mr":
        return MR_INTENT_RESPONSE_MAP.get(intent, "तुमच्या विनंतीवर प्रक्रिया केली आहे. कृपया पुढचा पर्याय निवडा.")
    return english_response


def translate_sub_options(options: list[str], target_language: str) -> list[str]:
    """Translate sub-option labels to requested language."""
    if target_language != "mr":
        return options
    return [EN_TO_MR_LABEL_MAP.get(opt, opt) for opt in options]


def translate_response(response_text: str, target_language: str) -> str:
    """Backward-compatible wrapper used by older imports."""
    if target_language == "mr":
        return MR_INTENT_RESPONSE_MAP.get("fallback", response_text)
    return response_text
