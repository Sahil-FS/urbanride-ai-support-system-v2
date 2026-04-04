from __future__ import annotations

import asyncio
from dataclasses import dataclass
import sys
from pathlib import Path
from textwrap import shorten

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.intent_client import detect_intent


@dataclass(frozen=True)
class Sample:
    language: str
    text: str
    expected_intent: str


SAMPLES: list[Sample] = [
    Sample("en", "The driver never showed up and I have been waiting for 25 minutes.", "driver_not_arrived"),
    Sample("en", "My ride is moving, but the driver is taking a much longer road than needed.", "long_route_taken"),
    Sample("en", "The payment was declined even though my card is valid.", "payment_failed"),
    Sample("en", "I was charged twice for the same trip today.", "double_payment"),
    Sample("en", "I want to cancel because the pickup time is too late.", "cancel_ride"),
    Sample("en", "I cannot reach the driver from the app call button.", "cannot_contact_driver"),
    Sample("en", "Please help me find my wallet that I forgot in the cab.", "lost_item"),
    Sample("en", "The driver was driving too fast and made me feel unsafe.", "rash_driving"),
    Sample("en", "I need a refund because the trip ended with the wrong fare.", "refund_request"),
    Sample("en", "My pickup pin is not matching the place where I am standing.", "wrong_pickup_location"),
    Sample("en", "The app keeps failing whenever I try to book a ride.", "app_not_working"),
    Sample("en", "I forgot my password and cannot log in.", "login_problem"),
    Sample("en", "I want to update my profile details and phone number.", "update_profile"),
    Sample("en", "How do I check the refund status for my last ride?", "refund_status"),
    Sample("en", "This driver behaved badly and spoke rudely to me.", "driver_misbehavior"),
    Sample("mr", "ड्रायव्हर अजून आला नाही आणि मी खूप वेळ वाट पाहतो आहे.", "driver_not_arrived"),
    Sample("mr", "राइड संपताना चुकीचे भाडे आकारले गेले आहे.", "wrong_fare_charged"),
    Sample("mr", "माझ्या कार्डमुळे पेमेंट नाकारले गेले.", "payment_failed"),
    Sample("mr", "माझ्याकडून एकाच प्रवासासाठी दोनदा पैसे कापले गेले.", "double_payment"),
    Sample("mr", "मला ही राइड आता रद्द करायची आहे.", "cancel_ride"),
    Sample("mr", "अॅपमधून ड्रायव्हरशी संपर्क होत नाही.", "cannot_contact_driver"),
    Sample("mr", "मी माझी पर्स गाडीत विसरले आहे.", "lost_item"),
    Sample("mr", "ड्रायव्हर खूप वेगाने आणि बेफिकिरीने चालवत होता.", "rash_driving"),
    Sample("mr", "मला परतफेड हवी आहे कारण भाडे चुकीचे लागले.", "refund_request"),
    Sample("mr", "पिकअप पिन मी उभा आहे त्या जागेशी जुळत नाही.", "wrong_pickup_location"),
    Sample("mr", "अॅप बुकिंगच्या वेळी वारंवार बंद पडत आहे.", "app_not_working"),
    Sample("mr", "मला माझा पासवर्ड आठवत नाही आणि लॉगिन होत नाही.", "login_problem"),
    Sample("mr", "मला प्रोफाइलमध्ये फोन नंबर बदलायचा आहे.", "update_profile"),
    Sample("mr", "माझ्या शेवटच्या राइडचा रिफंड स्टेटस काय आहे?", "refund_status"),
    Sample("mr", "ड्रायव्हरने उद्धटपणे वागून मला असुरक्षित वाटले.", "driver_misbehavior"),
    Sample("mr", "ड्रायव्हर योग्य वेळी येणार नसेल तर मी मोफत रद्द करू शकतो का?", "cancel_ride_free"),
    Sample("hi", "ड्राइवर अभी तक नहीं आया है और मैं काफी देर से इंतजार कर रहा हूँ।", "driver_not_arrived"),
    Sample("hi", "मेरी यात्रा में किराया गलत लगाया गया है।", "wrong_fare_charged"),
    Sample("hi", "कार्ड वैध होने के बावजूद भुगतान अस्वीकार हो गया।", "payment_failed"),
    Sample("hi", "मुझसे एक ही राइड के लिए दो बार शुल्क लिया गया।", "double_payment"),
    Sample("hi", "मुझे यह राइड अभी रद्द करनी है।", "cancel_ride"),
    Sample("hi", "ऐप से ड्राइवर को कॉल नहीं हो रहा है।", "cannot_contact_driver"),
    Sample("hi", "मैं अपना पर्स गाड़ी में भूल गया हूँ।", "lost_item"),
    Sample("hi", "ड्राइवर बहुत तेज़ और लापरवाही से चला रहा था।", "rash_driving"),
    Sample("hi", "मुझे रिफंड चाहिए क्योंकि किराया गलत लगा है।", "refund_request"),
    Sample("hi", "पिकअप पिन उस जगह से मेल नहीं खा रहा जहाँ मैं खड़ा हूँ।", "wrong_pickup_location"),
    Sample("hi", "बुकिंग के समय ऐप बार-बार फेल हो रहा है।", "app_not_working"),
    Sample("hi", "मुझे अपना पासवर्ड याद नहीं है और लॉगिन नहीं हो रहा।", "login_problem"),
    Sample("hi", "मुझे प्रोफ़ाइल में फोन नंबर बदलना है।", "update_profile"),
    Sample("hi", "मेरी पिछली राइड का रिफंड स्टेटस क्या है?", "refund_status"),
    Sample("hi", "ड्राइवर ने बदतमीज़ी की और मुझे असुरक्षित महसूस हुआ।", "driver_misbehavior"),
    Sample("hi", "अगर ड्राइवर समय पर नहीं आया तो क्या मैं फ्री में कैंसिल कर सकता हूँ?", "cancel_ride_free"),
]


async def run_sample(sample: Sample) -> tuple[str, float]:
    result = await detect_intent(sample.text)
    return result.intent, result.confidence


async def main() -> None:
    print("Multilingual intent evaluation")
    print("-" * 96)
    print(f"{'lang':<6} {'expected':<24} {'predicted':<24} {'score':<8} text")
    print("-" * 96)

    matches = 0
    for sample in SAMPLES:
        predicted_intent, confidence = await run_sample(sample)
        match = predicted_intent == sample.expected_intent
        matches += int(match)
        print(
            f"{sample.language:<6} {sample.expected_intent:<24} {predicted_intent:<24} {confidence:<8.4f} "
            f"{shorten(sample.text, width=72, placeholder='...')}"
        )

    print("-" * 96)
    print(f"Matched {matches}/{len(SAMPLES)} samples")


if __name__ == "__main__":
    asyncio.run(main())