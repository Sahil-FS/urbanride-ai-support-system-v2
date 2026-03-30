"""
chatbot_engine.py — Rule-based decision tree
Urban Black Taxi Ride — AI Chatbot Service
"""

import itertools
import logging
from app.core.config import settings
from app.services.state_service import get_state, set_state, clear_state

logger = logging.getLogger(__name__)


# ── CATEGORY 3 — Show call button IMMEDIATELY ─────────────────────────────────
ALWAYS_SHOW_CALL: set[str] = {
    "emergency_sos",
    "accident_report",
    "ride_started_without_user",
    "double_payment",
    "contact_support",
}

# ── CATEGORY 1 — Show sub-options after response ──────────────────────────────
INTENT_SUB_OPTIONS: dict[str, list[str]] = {

    # Ride tracking
    "track_ride": [
        "Driver Not Arrived",
        "Driver is Late",
        "Cannot Contact Driver",
    ],
    "driver_issue": [
        "Driver Not Arrived",
        "Driver is Late",
        "Cannot Contact Driver",
        "Driver Misbehavior",
    ],
    "driver_not_arrived": [
        "Contact Driver",
        "Cancel Ride for Free",
        "Call Support Now",
    ],
    "driver_late": [
        "Contact Driver",
        "Cancel Ride for Free",
        "Call Support Now",
    ],
    "cannot_contact_driver": [
        "Call Driver Again",
        "Send Message to Driver",
        "Cancel Ride for Free",
        "Get Help from Support",
    ],
    "still_need_help_driver_contact": [
        "Assign New Driver",
        "Cancel Ride for Free",
        "Call Support Now",
    ],
    "wrong_pickup_location": [
        "Contact Driver",
        "Update Pickup Pin",
        "Call Support Now",
    ],
    "ride_not_started": [
        "Ask Driver to Start",
        "Call Support Now",
    ],

    # Cancellation — top level only
    "cancel_ride": [
        "Cancel My Current Ride",
        "Cancel Ride for Free",
        "Driver Cancelled on Me",
        "Cancellation Fee Issue",
    ],

    # Payment — top level only
    "payment_issue": [
        "Payment Failed",
        "I Was Charged Twice",
        "Wrong Fare Charged",
        "Change Payment Method",
    ],
    "payment_failed": [
        "Retry Payment",
        "Change Payment Method",
        "Call Support Now",
    ],
    "wrong_fare_charged": [
        "Dispute the Fare",
        "Call Support Now",
    ],

    # Refund — top level only
    "refund_request": [
        "Check Refund Status",
        "Refund Not Received",
        "Request a New Refund",
    ],
    "invoice_request": [
        "Download Invoice",
        "Email Invoice",
        "Call Support Now",
    ],
    "refund_not_received": [
        "Escalate My Refund",
        "Call Support Now",
    ],

    # Safety — top level only
    "safety_issue": [
        "Driver Misbehavior",
        "Rash Driving",
        "SOS Emergency",
        "Accident Report",
    ],
    "driver_misbehavior": [
        "Report This Driver",
        "Call Support Now",
    ],
    "rash_driving": [
        "Report This Driver",
        "Call Support Now",
    ],

    # Lost item
    "lost_item": [
        "Contact My Driver",
        "Report Lost Item",
    ],

    # Account
    "account_issue": [
        "Login Problem",
        "Update My Profile",
        "Call Support Now",
    ],
    "login_problem": [
        "Reset Password",
        "Try Again",
        "Call Support Now",
    ],

    # Offers
    "apply_coupon": [
        "Retry the Coupon",
        "Check Offer Terms",
        "Call Support Now",
    ],
    "offer_not_applied": [
        "Retry the Coupon",
        "Call Support Now",
    ],

    # Route
    "route_issue": [
        "Driver Took Long Route",
        "Dispute the Route",
        "Call Support Now",
    ],
    "long_route_taken": [
        "Dispute the Fare",
        "Call Support Now",
    ],

    # Fallback
    "unknown_intent": ["Call Support Now"],
    "fallback":        ["Call Support Now"],
}


# ── ALL RESPONSES ─────────────────────────────────────────────────────────────
INTENT_RESPONSES: dict[str, list[str]] = {

    # General
    "greeting": [
        "Hello! 👋 Welcome to Urban Taxi Support. How can I help you today?",
    ],
    "goodbye": [
        "Thank you for contacting Urban Taxi Support. Have a safe ride! 🚕",
    ],
    "thank_you": [
        "You are welcome! Is there anything else I can help you with?",
    ],
    "help_request": [
        "I am here to help! You can ask me about ride tracking, payments, "
        "driver issues, lost items, or account help. What is your concern?",
    ],

    # Ride tracking
    "track_ride": [
        "You can track your ride in real-time from the app map. "
        "Once your ride is booked, your driver’s live location will be visible on the map. "
        "If you're facing any issue with your ride or driver, please select an option below:",
    ],
    "driver_issue": [
        "I can help you with driver-related issues. Please select the problem you are facing:",
    ],
    "driver_not_arrived": [
        "Sorry your driver has not arrived yet. Please check the live map in the app. "
        "You can also call or message your driver directly from the ride screen. "
        "What would you like to do?",
    ],
    "driver_late": [
        "We apologize for the delay. Your driver is on the way. "
        "You can track their live location on the map. "
        "If the delay is too long, you may contact the driver or cancel the ride. "
        "What would you like to do?",
    ],
    "cannot_contact_driver": [
        "It looks like your driver is not responding. "
        "You can try calling again, send a message, or take action like cancelling or getting help.",
    ],
    "still_need_help_driver_contact": [
        "We understand you're unable to reach the driver. "
        "We will take action and can assign you a new driver if needed.",
    ],
    "report_driver_contact_issue": [
        "✅ Your issue has been reported. "
        "Our team will check why the driver is unreachable and take action if needed. "
        "You may be assigned a new driver shortly.",
    ],
    "wrong_pickup_location": [
        "Please confirm your pickup location with the driver via in-app chat. "
        "You can also update your pickup pin on the map. What would you like to do?",
    ],
    "wrong_drop_location": [
        "To change your drop-off point during a ride, tap the destination bar "
        "at the top of the map and enter the new address. This can be done anytime during the trip.",
    ],
    "ride_started_without_user": [
        "🚨 This is a serious issue! Please stay calm. "
        "Our safety team is being alerted immediately. "
        "You will NOT be charged for this ride. Please call our support team right now:",
    ],
    "ride_not_started": [
        "If the driver is present but the trip has not started, "
        "ask them to start it from their driver app. "
        "If they refuse or are unresponsive, please select an option below:",
    ],

    # Cancellation — top level
    "cancel_ride": [
        "I can help you with your cancellation. What is the situation?",
    ],

    # ✅ SPECIFIC cancellation outcomes — no more looping
    "cancel_ride_now": [
        "✅ Your ride cancellation request has been submitted. "
        "If a cancellation fee applies it will be shown in your trip history. "
        "You can rebook a new ride anytime from the home screen.",
    ],
    "cancel_ride_free": [
        "✅ Since your driver has not arrived within the expected time, "
        "you are eligible for a free cancellation. "
        "Your ride has been cancelled with no charge. "
        "Please rebook and a new driver will be assigned shortly.",
    ],
    "cancel_by_driver": [
        "We sincerely apologize that your driver cancelled your ride. "
        "Our system will attempt to find you a new driver shortly. "
        "You will not be charged anything. If this keeps happening please report it.",
    ],
    "cancellation_fee_issue": [
        "If you believe the cancellation fee was applied incorrectly, "
        "we will review your case within 24 hours and refund if eligible. "
        "Our team will reach out to you shortly.",
    ],
    "dispute_fee": [
        "✅ Your cancellation fee dispute has been submitted. "
        "Our billing team will review your ride timeline and GPS data. "
        "If the fee was incorrect, a refund will be processed within 3-5 business days.",
    ],

    # Payments — top level
    "payment_issue": [
        "I can help with your payment concern. "
        "What type of payment issue are you facing?",
    ],

    # ✅ SPECIFIC payment outcomes
    "payment_failed": [
        "Your payment may have failed due to an expired card or insufficient balance. "
        "Please update your payment method under Profile → Payments and retry. "
        "If the amount was deducted but the ride failed, "
        "it will be automatically refunded within 3-5 business days.",
    ],
    "double_payment": [
        "🚨 We are sorry you were charged twice. "
        "This will be investigated and the duplicate amount refunded immediately. "
        "Please call our billing team now to expedite this:",
    ],
    "wrong_fare_charged": [
        "If you were overcharged we will investigate and correct it. "
        "What would you like to do?",
    ],
    "payment_method_change": [
        "To add or change a payment method, go to Profile → Payments → "
        "Add Payment Method and follow the prompts. "
        "Changes take effect immediately for your next ride.",
    ],

    # ✅ Dispute outcomes
    "dispute_charge": [
        "✅ Your billing dispute has been registered. "
        "Our team will review the charge and GPS data within 24 hours. "
        "If an error is found, the refund will be processed within 3-5 business days.",
    ],
    "dispute_fare": [
        "✅ Your fare dispute has been submitted successfully. "
        "We will review your trip's GPS route and fare calculation. "
        "If overcharged, the difference will be refunded within 3-5 business days.",
    ],
    "dispute_route": [
        "✅ Your route dispute has been submitted. "
        "Our team will review the GPS data from your trip. "
        "If the driver took an unnecessarily long route, "
        "you will receive a fare adjustment within 24 hours.",
    ],

    # Refunds — top level
    "refund_request": [
        "I can help with your refund. What would you like to know?",
    ],

    # ✅ SPECIFIC refund outcomes
    "refund_status": [
        "Refunds typically take 5-7 business days to reflect in your account. "
        "You can check status under My Rides → select the trip → Refund Status. "
        "If it has been more than 7 days, please use the escalate option.",
    ],
    "refund_not_received": [
        "If your refund has not arrived after 7 business days we will escalate it. "
        "What would you like to do?",
    ],
    "refund_initiated": [
        "✅ Your refund request has been initiated successfully. "
        "The amount will be credited to your original payment method "
        "within 5-7 business days. You will receive a confirmation SMS shortly.",
    ],
    "escalate_refund": [
        "✅ Your refund has been escalated to our priority team. "
        "A senior agent will review your case within 4 hours "
        "and reach out to you on your registered mobile number.",
    ],
    "invoice_request": [
        "You can download your trip invoice from My Rides → select the trip → "
        "Download Invoice. It is also emailed to your registered address after every trip.",
    ],
    "fare_breakup": [
        "Your fare includes: Base Fare + Per KM charge + Time charge + Taxes. "
        "See the complete breakup under My Rides → select the trip → Fare Details.",
    ],

    # Safety — top level
    "safety_issue": [
        "Your safety is our absolute top priority. "
        "Please tell me more about the safety concern you are facing:",
    ],

    # ✅ SPECIFIC safety outcomes
    "driver_misbehavior": [
        "🚨 We take driver conduct extremely seriously. "
        "Your report is completely confidential. "
        "We will take strict action against this driver within 24 hours. "
        "Would you like to report formally or speak to our team directly?",
    ],
    "rash_driving": [
        "🚨 We sincerely apologize for this experience. "
        "Rash driving is a serious violation of our driver policy. "
        "You can end the trip at any time by asking the driver to stop safely. "
        "What would you like to do?",
    ],
    "accident_report": [
        "🚨 Please ensure your safety first. "
        "Call emergency services (112) immediately if anyone is injured. "
        "Our safety team is standing by. Please call us right now:",
    ],
    "emergency_sos": [
        "🚨 EMERGENCY DETECTED. "
        "Please use the SOS button (shield icon) inside your active ride screen RIGHT NOW. "
        "This alerts emergency services AND our safety team simultaneously. "
        "Or call us directly right now:",
    ],
    "report_driver": [
        "✅ Your driver complaint has been submitted and is marked confidential. "
        "Our safety team will review the trip recording and take strict action "
        "within 24 hours. You will receive an update on your registered number.",
    ],

    # Lost item
    "lost_item": [
        "Sorry to hear that! Go to My Rides → select the completed trip → "
        "Find Lost Item to connect with your driver. "
        "A small return fee may apply if the driver delivers the item. "
        "What would you like to do?",
    ],
    "contact_driver": [
        "You can contact your driver directly from the active ride screen. "
        "Tap the phone icon to call or the chat icon to message. "
        "If the trip is completed, use My Rides → Find Lost Item to reconnect.",
    ],
    "report_lost_item": [
        "✅ Your lost item report has been submitted. "
        "We will contact your driver immediately. "
        "You will receive a response within 30 minutes on your registered number.",
    ],

    # Account
    "account_issue": [
        "I can help with your account. What type of issue are you facing?",
    ],
    "login_problem": [
        "Try resetting your login by tapping Forgot Password on the login screen. "
        "A one-time password will be sent to your registered mobile number. "
        "Note: phone number and email changes require OTP re-verification before saving. "
        "If the issue persists after 3 attempts, please contact our support team.",
    ],
    "update_profile": [
        "To update your profile, go to Profile → tap Edit Profile. "
        "You can update your name, email, phone number, and photo. "
        "Changes are saved immediately.",
    ],

    # Offers
    "apply_coupon": [
        "Enter promo codes at the checkout screen before confirming your ride. "
        "Tap Enter Promo Code on the fare summary screen. "
        "Codes cannot be applied after a trip is already booked.",
    ],
    "offer_not_applied": [
        "Please check the offer terms and expiry date. "
        "Make sure you entered the code correctly before booking. "
        "What would you like to do?",
    ],
    "retry_coupon": [
        "Please double-check the coupon code spelling and expiry date. "
        "If the code is valid and still not working, "
        "our team will manually apply the discount for you. Please contact support.",
    ],

    # Route
    "route_issue": [
        "I can help with a route concern. What happened?",
    ],
    "long_route_taken": [
        "If your driver took a longer route than necessary you can dispute the fare "
        "and we will review the GPS data. What would you like to do?",
    ],

    # Support
    "contact_support": [
        "Connecting you to our support team now. "
        "Please tap the button below to call us directly. "
        "Our team is available 24/7:",
    ],

    # Fallback
    "unknown_intent": [
        "I was not able to understand your request clearly. "
        "Please try rephrasing, or connect with a live agent who can help you immediately:",
    ],
    "fallback": [
        "I'm not sure I understood that. Please choose an option below or try again. "
        "If the issue continues, you can contact our support team."
    ],
}


# ── PILL LABEL → INTENT OVERRIDE MAP ─────────────────────────────────────────
# This maps pill text directly to a specific intent
# so sub-option clicks NEVER loop back to the parent question
PILL_INTENT_MAP: dict[str, str] = {
    # Frontend labels
    "driver issue":   "driver_issue",
    "track ride":     "track_ride",
    "payment issue":  "payment_issue",
    "refund request": "refund_request",
    "safety concern": "safety_issue",

    # Cancel pills
    "cancel my current ride":  "cancel_ride_now",
    "driver cancelled on me":  "cancel_by_driver",
    "cancellation fee issue":  "cancellation_fee_issue",
    "dispute the fee":         "dispute_fee",

    # Payment pills
    "payment failed":          "payment_failed",
    "i was charged twice":     "double_payment",
    "wrong fare charged":      "wrong_fare_charged",
    "change payment method":   "payment_method_change",
    "dispute the fare":        "dispute_fare",
    "dispute the charge":      "dispute_charge",

    # Refund pills
    "check refund status":     "refund_status",
    "refund not received":     "refund_not_received",
    "request a new refund":    "refund_initiated",
    "escalate my refund":      "escalate_refund",

    # Safety pills
    "driver misbehavior":      "driver_misbehavior",
    "rash driving":            "rash_driving",
    "sos emergency":           "emergency_sos",
    "accident report":         "accident_report",
    "report this driver":      "report_driver",

    # Route pills
    "driver took long route":  "long_route_taken",
    "dispute the route":       "dispute_route",

    # Lost item pills
    "contact my driver":       "contact_driver",
    "report lost item":        "report_lost_item",

    # Ride pills
    "driver not arrived":      "driver_not_arrived",
    "driver is late":          "driver_late",
    "cannot contact driver":   "cannot_contact_driver",
    "contact driver":          "contact_driver",
    "cancel ride for free":    "cancel_ride_free",
    "ask driver to start":     "ride_not_started",

    # Account pills
    "login problem":           "login_problem",
    "update my profile":       "update_profile",

    # Offer pills
    "retry the coupon":        "retry_coupon",

    # Support pills
    "call support now":        "contact_support",
    "talk to support":         "contact_support",
    "retry payment":           "payment_method_change",
    "call driver again":        "contact_driver",
    "send message to driver":   "contact_driver",
    "get help from support":    "contact_support",
    "assign new driver":        "driver_not_arrived",
    "still need help":         "still_need_help_driver_contact",
    "raise driver contact issue": "report_driver_contact_issue",
    "reset password":          "login_problem",
    "try again":               "login_problem",
    "download invoice":        "invoice_request",
    "email invoice":           "invoice_request",
    "check offer terms":       "offer_not_applied",
}


# ── Round-robin iterators ─────────────────────────────────────────────────────
_iterators: dict[str, itertools.cycle] = {
    intent: itertools.cycle(responses)
    for intent, responses in INTENT_RESPONSES.items()
}


# ── Public API ────────────────────────────────────────────────────────────────
CALL_TRIGGER_MESSAGES: set[str] = {
    "call support now",
    "call customer support",
    "call support",
    "talk to support",
    "talk to agent",
    "speak to agent",
    "human agent",
    "live agent",
    "phone support",
}


def is_call_trigger(message: str) -> bool:
    return message.lower().strip() in CALL_TRIGGER_MESSAGES


def get_response(intent: str, confidence: float, original_text: str = "", user_id: int = 1) -> dict:
    """
    Decision tree:
      0. Pill override      → direct specific intent (NO loops)
      1. Low confidence     → fallback + call button
      2. Unknown intent     → unknown_intent + call button
      3. Category 3         → response + call button immediately
      4. Category 1         → response + sub-options
      5. Category 2         → direct response only
    """

    # Branch 0 — pill label override (prevents ALL looping)
    pill_key = original_text.lower().strip()

    # ── STATE MANAGEMENT ─────────────────────────────

    state = get_state(user_id)

    # ── AUTO RESET FOR NEW FLOW ──────────────────────────────

    TOP_LEVEL_INTENTS = {
        "track_ride",
        "driver_issue",
        "payment_issue",
        "cancel_ride",
        "refund_request",
        "safety_issue",
        "account_issue",
        "lost_item",
    }

    if intent in TOP_LEVEL_INTENTS and len(state.get("flow_history", [])) > 1:
        state["flow_history"] = [intent]
        state["flow_completed"] = False
        state["escalated"] = False
        set_state(user_id, state)

    # ── FLOW TRACKING ─────────────────────────────

    if "flow_history" not in state:
        state["flow_history"] = []

    if intent not in state["flow_history"]:
        state["flow_history"].append(intent)

    state["last_intent"] = intent

    set_state(user_id, state)

    # Clean post-flow behavior
    if state.get("flow_completed") and intent not in TOP_LEVEL_INTENTS and pill_key not in ["helpful", "not helpful", "escalate"]:
        return {
            "resolved_intent": intent,
            "response": "✅ Your issue has already been resolved. Let me know if you need anything else.",
            "sub_options": [],
            "show_call_button": False,
        }

    # Allow feedback even after escalation
    if state.get("escalated") and pill_key not in ["helpful", "not helpful", "escalate"]:
        return {
            "resolved_intent": intent,
            "response": "📞 Your issue is already escalated. Our team will contact you shortly.",
            "sub_options": [],
            "show_call_button": True,
        }

    # Helpful feedback
    if pill_key == "helpful":
        clear_state(user_id)
        return {
            "resolved_intent": "feedback",
            "response": "😊 Glad we could help you!",
            "sub_options": [],
            "show_call_button": False,
        }

    # Not helpful feedback
    if pill_key == "not helpful":
        clear_state(user_id)
        return {
            "resolved_intent": "feedback",
            "response": "📞 I understand this didn't help. You can connect with our support team.",
            "sub_options": ["Call Support Now"],
            "show_call_button": True,
        }

    # Escalation handling
    if pill_key == "escalate":
        state["escalated"] = True
        state["flow_completed"] = True

        flow = state.get("flow_history", [])

        if any(i in flow for i in ["driver_not_arrived", "driver_late", "cannot_contact_driver"]):
            msg = "🚗 Your issue has been escalated to our driver support team. You will be contacted within 30 minutes."

        elif any(i in flow for i in ["payment_failed", "double_payment", "wrong_fare_charged"]):
            msg = "💰 Your payment issue has been escalated. Refund will be processed within 3–5 business days."

        elif any(i in flow for i in ["refund_not_received", "refund_request"]):
            msg = "💸 Your refund issue has been escalated to priority support. You will receive an update within 4 hours."

        elif any(i in flow for i in ["driver_misbehavior", "rash_driving", "safety_issue"]):
            msg = "🚨 Your safety issue has been escalated immediately. Our safety team is reviewing this on priority."

        else:
            msg = "📞 Your issue has been escalated to our support team. You will be contacted shortly."

        set_state(user_id, state)

        return {
            "resolved_intent": "escalated",
            "response": msg,
            "sub_options": [],
            "show_call_button": True,
        }
    if pill_key in PILL_INTENT_MAP:
        overridden_intent = PILL_INTENT_MAP[pill_key]
        if overridden_intent in INTENT_RESPONSES:
            intent = overridden_intent

    # Branch 0.5 — direct call trigger
    if is_call_trigger(original_text):
        state["flow_completed"] = True
        set_state(user_id, state)
        return {
            "resolved_intent": "contact_support",
            "response": next(_iterators["contact_support"]),
            "sub_options": [],
            "show_call_button": True,
        }

    # Branch 1 — low confidence
    if confidence < settings.CONFIDENCE_THRESHOLD and pill_key not in PILL_INTENT_MAP:
        return {
            "resolved_intent": "fallback",
            "response": next(_iterators["fallback"]),
            "sub_options": [],
            "show_call_button": True,
        }

    # Branch 2 — intent not in catalogue
    if intent not in INTENT_RESPONSES:
        return {
            "resolved_intent": "unknown_intent",
            "response": next(_iterators["unknown_intent"]),
            "sub_options": [],
            "show_call_button": True,
        }

    # Branch 3 — Category 3 (emergency/serious — call button immediately)
    if intent in ALWAYS_SHOW_CALL:
        return {
            "resolved_intent": intent,
            "response": next(_iterators[intent]),
            "sub_options": INTENT_SUB_OPTIONS.get(intent, []),
            "show_call_button": True,
        }

    # Branch 4 — Category 1 (broad — show sub-options)
    if intent in INTENT_SUB_OPTIONS:
        return {
            "resolved_intent": intent,
            "response": next(_iterators[intent]),
            "sub_options": INTENT_SUB_OPTIONS[intent],
            "show_call_button": False,
        }

    # Branch 5 — Category 2 (specific — direct response, no sub-options)
    # Mark flow completed for terminal intents
    terminal_intents = {
        "cancel_ride_now",
        "cancel_ride_free",
        "report_driver",
        "refund_initiated",
        "dispute_fare",
        "dispute_charge",
        "report_lost_item",
        "dispute_route",
        "contact_support",
        "escalated",
        "emergency_sos",
    }

    if intent in terminal_intents:
        state["flow_completed"] = True
        set_state(user_id, state)

    return {
        "resolved_intent": intent,
        "response": next(_iterators[intent]),
        "sub_options": [],
        "show_call_button": False,
    } 