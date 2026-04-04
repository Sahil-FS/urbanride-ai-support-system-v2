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

EN_TO_HI_LABEL_MAP: dict[str, str] = {
    "Track Ride": "राइड ट्रैक करें",
    "Driver Issue": "ड्राइवर समस्या",
    "Payment Issue": "भुगतान समस्या",
    "Cancel Ride": "राइड रद्द करें",
    "Refund Request": "रिफंड अनुरोध",
    "Safety Concern": "सुरक्षा चिंता",
    "Talk to Support": "सपोर्ट से बात करें",
    "Driver Not Arrived": "ड्राइवर नहीं आया",
    "Driver is Late": "ड्राइवर देर से है",
    "Cannot Contact Driver": "ड्राइवर से संपर्क नहीं हो रहा",
    "Contact Driver": "ड्राइवर से संपर्क करें",
    "Cancel Ride for Free": "राइड बिना शुल्क रद्द करें",
    "Call Support Now": "कस्टमर सपोर्ट को कॉल करें",
    "Report Issue": "समस्या दर्ज करें",
    "Update Pickup Pin": "पिकअप पिन अपडेट करें",
    "Ask Driver to Start": "ड्राइवर से राइड शुरू करने को कहें",
    "Cancel My Current Ride": "मेरी वर्तमान राइड रद्द करें",
    "Driver Cancelled on Me": "ड्राइवर ने मेरी राइड रद्द की",
    "Cancellation Fee Issue": "रद्दीकरण शुल्क समस्या",
    "Dispute the Fee": "शुल्क पर आपत्ति दर्ज करें",
    "Payment Failed": "भुगतान विफल",
    "I Was Charged Twice": "मुझसे दो बार शुल्क लिया गया",
    "Wrong Fare Charged": "गलत किराया वसूला गया",
    "Change Payment Method": "भुगतान तरीका बदलें",
    "Dispute the Fare": "किराए पर आपत्ति दर्ज करें",
    "Dispute the Charge": "शुल्क पर आपत्ति दर्ज करें",
    "Check Refund Status": "रिफंड स्थिति देखें",
    "Refund Not Received": "रिफंड नहीं मिला",
    "Request a New Refund": "नया रिफंड अनुरोध करें",
    "Escalate My Refund": "मेरा रिफंड एस्केलेट करें",
    "Driver Misbehavior": "ड्राइवर का अनुचित व्यवहार",
    "Rash Driving": "लापरवाही से ड्राइविंग",
    "SOS Emergency": "SOS आपातकाल",
    "Accident Report": "दुर्घटना रिपोर्ट",
    "Report This Driver": "इस ड्राइवर की रिपोर्ट करें",
    "Contact My Driver": "मेरे ड्राइवर से संपर्क करें",
    "Report Lost Item": "खोई वस्तु रिपोर्ट करें",
    "Login Problem": "लॉगिन समस्या",
    "Update My Profile": "अपनी प्रोफ़ाइल अपडेट करें",
    "Retry the Coupon": "कूपन फिर से आज़माएँ",
    "Driver Took Long Route": "ड्राइवर ने लंबा रास्ता लिया",
    "Dispute the Route": "रूट पर आपत्ति दर्ज करें",
}

EN_TO_HI_LABEL_MAP.update(
    {
        "🚕 Track Ride": "🚕 राइड ट्रैक करें",
        "👤 Driver Issue": "👤 ड्राइवर समस्या",
        "💳 Payment Issue": "💳 भुगतान समस्या",
        "❌ Cancel Ride": "❌ राइड रद्द करें",
        "💰 Refund Request": "💰 रिफंड अनुरोध",
        "🆘 Safety Concern": "🆘 सुरक्षा चिंता",
        "📞 Talk to Support": "📞 सपोर्ट से बात करें",
    }
)

MR_TO_EN_LABEL_MAP: dict[str, str] = {v.lower(): k for k, v in EN_TO_MR_LABEL_MAP.items()}
HI_TO_EN_LABEL_MAP: dict[str, str] = {v.lower(): k for k, v in EN_TO_HI_LABEL_MAP.items()}

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

LANGUAGE_LABEL_MAPS: dict[str, dict[str, str]] = {
    "mr": EN_TO_MR_LABEL_MAP,
    "hi": EN_TO_HI_LABEL_MAP,
}

LANGUAGE_TO_EN_LABEL_MAPS: dict[str, dict[str, str]] = {
    "mr": MR_TO_EN_LABEL_MAP,
    "hi": HI_TO_EN_LABEL_MAP,
}


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

HI_INTENT_RESPONSE_MAP: dict[str, str] = {
    "greeting": "नमस्ते! 👋 अर्बन टैक्सी सपोर्ट में आपका स्वागत है। आज मैं आपकी कैसे मदद कर सकता हूँ?",
    "goodbye": "अर्बन टैक्सी सपोर्ट से संपर्क करने के लिए धन्यवाद। आपकी यात्रा सुरक्षित रहे! 🚕",
    "thank_you": "आपका स्वागत है! क्या मैं और किसी चीज़ में मदद कर सकता हूँ?",
    "help_request": "मैं मदद के लिए यहाँ हूँ। आप राइड ट्रैकिंग, भुगतान, ड्राइवर समस्या, खोई वस्तु या अकाउंट सहायता के बारे में पूछ सकते हैं।",
    "track_ride": "मैं आपकी राइड की स्थिति में मदद कर सकता हूँ। ड्राइवर को लेकर क्या समस्या है?",
    "driver_not_arrived": "क्षमा करें, आपका ड्राइवर अभी तक नहीं पहुँचा है। कृपया ऐप में लाइव मैप देखें।",
    "driver_late": "देरी के लिए क्षमा करें। आपका ड्राइवर रास्ते में है। कृपया लाइव मैप देखें।",
    "cannot_contact_driver": "ऐप की राइड स्क्रीन से ड्राइवर को कॉल करके देखें। अगर जवाब नहीं मिले, तो नीचे दिया गया विकल्प चुनें।",
    "wrong_pickup_location": "कृपया ऐप चैट के जरिए ड्राइवर से पिकअप लोकेशन कन्फर्म करें। आप पिकअप पिन भी अपडेट कर सकते हैं।",
    "ride_not_started": "अगर ड्राइवर मौजूद है लेकिन राइड शुरू नहीं हुई है, तो ड्राइवर से ऐप में राइड शुरू करने को कहें।",
    "cancel_ride": "मैं राइड रद्द करने में मदद कर सकता हूँ। स्थिति क्या है?",
    "cancel_ride_now": "आपका राइड कैंसलेशन अनुरोध भेज दिया गया है। लागू शुल्क ट्रिप हिस्ट्री में दिखेगा।",
    "cancel_ride_free": "ड्राइवर समय पर नहीं पहुँचा, इसलिए आप बिना शुल्क रद्द करने के पात्र हैं। आपकी राइड बिना किसी शुल्क के रद्द कर दी गई है।",
    "cancel_by_driver": "क्षमा करें, ड्राइवर ने आपकी राइड रद्द कर दी। कुछ मिनटों में नया ड्राइवर असाइन कर दिया जाएगा।",
    "cancellation_fee_issue": "यदि रद्दीकरण शुल्क गलत लगा है, तो हमारी टीम 24 घंटों में इसकी जांच करेगी।",
    "dispute_fee": "आपकी रद्दीकरण शुल्क आपत्ति दर्ज कर ली गई है। जांच के बाद पात्र होने पर रिफंड किया जाएगा।",
    "payment_issue": "मैं भुगतान समस्या में मदद कर सकता हूँ। आपको किस प्रकार की भुगतान समस्या है?",
    "payment_failed": "भुगतान विफल होने का कारण कार्ड या बैलेंस की समस्या हो सकता है। कृपया भुगतान तरीका अपडेट करके फिर कोशिश करें।",
    "double_payment": "आपसे दो बार शुल्क लिए जाने के लिए क्षमा करें। इसकी तुरंत जांच होगी और डुप्लिकेट राशि वापस की जाएगी।",
    "wrong_fare_charged": "अगर आपसे गलत किराया वसूला गया है, तो हम इसकी जांच करेंगे। आगे आप क्या करना चाहेंगे?",
    "dispute_fare": "आपकी किराया आपत्ति सफलतापूर्वक दर्ज कर ली गई है। पात्र होने पर अंतर की राशि वापस की जाएगी।",
    "refund_request": "मैं रिफंड के मामले में मदद कर सकता हूँ। आपको क्या जानना है?",
    "refund_status": "रिफंड आमतौर पर 5-7 कार्यदिवस में खाते में दिखता है। 7 दिन से ज़्यादा होने पर एस्केलेट करें।",
    "refund_not_received": "7 दिन बाद भी रिफंड न मिले तो हम इसे एस्केलेट करेंगे।",
    "refund_initiated": "आपका रिफंड अनुरोध सफलतापूर्वक शुरू हो गया है। राशि 5-7 कार्यदिवस में जमा हो जाएगी।",
    "escalate_refund": "आपका रिफंड प्रायोरिटी टीम को एस्केलेट कर दिया गया है। वरिष्ठ एजेंट 4 घंटे में जांच करेगा।",
    "safety_issue": "आपकी सुरक्षा हमारे लिए सबसे महत्वपूर्ण है। कृपया समस्या विस्तार से बताएं।",
    "driver_misbehavior": "ड्राइवर का अनुचित व्यवहार गंभीर है। आपकी शिकायत गोपनीय रहेगी और 24 घंटों में कार्रवाई की जाएगी।",
    "rash_driving": "लापरवाही से ड्राइविंग एक गंभीर उल्लंघन है। ज़रूरत हो तो आप सुरक्षित जगह पर राइड रोक सकते हैं।",
    "accident_report": "कृपया पहले अपनी सुरक्षा सुनिश्चित करें। अगर कोई घायल है, तो तुरंत 112 पर कॉल करें।",
    "emergency_sos": "🚨 आपात स्थिति पहचान ली गई है। कृपया सक्रिय राइड स्क्रीन में SOS बटन तुरंत इस्तेमाल करें।",
    "report_driver": "आपकी ड्राइवर शिकायत गोपनीय रूप से दर्ज कर ली गई है। 24 घंटों में कार्रवाई की जाएगी।",
    "lost_item": "खोई वस्तु वापस पाने के लिए My Rides में संबंधित ट्रिप खोलकर Find Lost Item का इस्तेमाल करें।",
    "contact_support": "हम आपको सपोर्ट टीम से जोड़ रहे हैं। कृपया नीचे दिए गए बटन से सीधे कॉल करें।",
    "login_problem": "लॉगिन स्क्रीन पर Forgot Password का उपयोग करके रीसेट करें। समस्या बनी रहे तो सपोर्ट से संपर्क करें।",
    "update_profile": "Profile → Edit Profile में जाकर आप नाम, ईमेल, फोन और फोटो अपडेट कर सकते हैं।",
    "route_issue": "मैं रूट से जुड़ी समस्या में मदद कर सकता हूँ। क्या हुआ, बताइए।",
    "long_route_taken": "अगर ड्राइवर ने जरूरत से लंबा रास्ता लिया है, तो आप किराए पर आपत्ति दर्ज कर सकते हैं। हम GPS डेटा जांचेंगे।",
    "unknown_intent": "मैं आपका अनुरोध स्पष्ट रूप से समझ नहीं पाया। कृपया फिर से लिखें या सीधे सपोर्ट से संपर्क करें।",
    "fallback": "मैं आपका अनुरोध स्पष्ट रूप से समझ नहीं पाया। कृपया फिर से लिखें या सीधे सपोर्ट से संपर्क करें।",
}


def normalize_user_message(text: str) -> str:
    """Convert known localized UI labels into canonical English labels for intent routing."""
    if not text:
        return text
    normalized = text.strip()
    normalized_lower = normalized.lower()

    # 1) Localized UI label to English canonical label.
    for language_map in LANGUAGE_TO_EN_LABEL_MAPS.values():
        mapped_label = language_map.get(normalized_lower)
        if mapped_label:
                        canonical = _strip_quick_reply_icon(mapped_label)
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
    for language_map in LANGUAGE_TO_EN_LABEL_MAPS.values():
        mapped_label = language_map.get(stripped_lower)
        if mapped_label:
            canonical = _strip_quick_reply_icon(mapped_label)
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
    language_map = {
        "mr": MR_INTENT_RESPONSE_MAP,
        "hi": HI_INTENT_RESPONSE_MAP,
    }.get(target_language)
    if language_map is not None:
        return language_map.get(intent, english_response)
    return english_response


def translate_sub_options(options: list[str], target_language: str) -> list[str]:
    """Translate sub-option labels to requested language."""
    language_map = LANGUAGE_LABEL_MAPS.get(target_language)
    if language_map is None:
        return options
    return [language_map.get(opt, opt) for opt in options]


def translate_response(response_text: str, target_language: str) -> str:
    """Backward-compatible wrapper used by older imports."""
    if target_language == "mr":
        return MR_INTENT_RESPONSE_MAP.get("fallback", response_text)
    if target_language == "hi":
        return HI_INTENT_RESPONSE_MAP.get("fallback", response_text)
    return response_text
