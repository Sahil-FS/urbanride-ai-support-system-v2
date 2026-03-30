from app.services.ticket_service import create_ticket
from app.services.ride_service import get_active_ride
from app.services.driver_service import get_driver
from app.services.payment_service import get_payment_status, get_refund_status
from app.services.issue_service import create_issue
from app.services.state_service import get_state, increment_fallback

INTENT_ALIASES = {
    # Ride/Track
    "DRIVER_LATE":           "TRACK_RIDE",
    "DRIVER_IS_LATE":        "TRACK_RIDE",
    "LATE_DRIVER":           "TRACK_RIDE",
    "TRACK":                 "TRACK_RIDE",
    "RIDE_TRACK":            "TRACK_RIDE",
    "CANNOT_CONTACT_DRIVER": "TRACK_RIDE",
    "DRIVER_NOT_ARRIVED":    "TRACK_RIDE",
    "LONG_ROUTE_TAKEN":      "TRACK_RIDE",
    "RIDE_NOT_STARTED":      "TRACK_RIDE",
    "ROUTE_ISSUE":           "TRACK_RIDE",
    "SCHEDULED_RIDE_ISSUE":  "TRACK_RIDE",
    "WRONG_DROP_LOCATION":   "TRACK_RIDE",
    "WRONG_PICKUP_LOCATION": "TRACK_RIDE",
    "CANCEL_BY_DRIVER":      "CANCEL_RIDE",

    # Payment
    "PAYMENT_ISSUE":         "PAYMENT_FAILED",
    "PAYMENT_ERROR":         "PAYMENT_FAILED",
    "DOUBLE_PAYMENT":        "BILLING_ISSUE",
    "CANCELLATION_FEE_ISSUE":"BILLING_ISSUE",
    "FARE_BREAKUP":          "BILLING_ISSUE",
    "INVOICE_REQUEST":       "BILLING_ISSUE",
    "PAYMENT_METHOD_CHANGE": "BILLING_ISSUE",
    "WRONG_FARE_CHARGED":    "BILLING_ISSUE",

    # Safety/Emergency
    "SAFETY":                "SAFETY_CONCERN",
    "SAFETY_ISSUE":          "SAFETY_CONCERN",
    "ACCIDENT_REPORT":       "SAFETY_CONCERN",
    "RIDE_STARTED_WITHOUT_USER": "SAFETY_CONCERN",
    "SOS_EMERGENCY":         "SOS",
    "EMERGENCY_SOS":         "SOS",
    "DRIVER_BAD":            "DRIVER_MISBEHAVIOR",
    "DRIVER_MISBEHAVING":    "SAFETY_CONCERN",
    "MISBEHAVIOR":           "DRIVER_MISBEHAVIOR",
    "DRIVER_MISBEHAVIOR":    "SAFETY_CONCERN",

    # Account
    "LOGIN_PROBLEM":         "ACCOUNT_ISSUE",
    "UPDATE_PROFILE":        "ACCOUNT_ISSUE",
    "HELP_REQUEST":          "GENERAL_HELP",
    "APP_NOT_WORKING":       "TECHNICAL_ISSUE",

    # Promos
    "OFFER_NOT_APPLIED":     "PROMO_ISSUE",
    "APPLY_COUPON":          "PROMO_ISSUE",

    # Refunds
    "REFUND_REQUEST":        "REFUND_ISSUE",
    "REFUND_STATUS":         "REFUND_ISSUE",
    "REFUND_NOT_RECEIVED":   "REFUND_ISSUE",

    # General
    "GOODBYE":               "GREETING",
    "THANK_YOU":             "GREETING",
    "UNKNOWN_INTENT":        "UNKNOWN"
}

INTENT_GROUPS = {
    "ride": [
        "track_ride", "driver_late", "driver_not_arrived",
        "cannot_contact_driver", "wrong_pickup_location",
        "wrong_drop_location", "ride_not_started",
        "ride_started_without_user", "route_issue", "long_route_taken"
    ],
    "payment": [
        "payment_failed", "payment_issue", "double_payment",
        "wrong_fare_charged", "refund_request",
        "refund_status", "refund_not_received"
    ],
    "safety": [
        "safety_issue", "driver_misbehavior",
        "rash_driving", "accident_report", "emergency_sos"
    ],
    "account": [
        "account_issue", "login_problem",
        "update_profile"
    ],
    "general": [
        "greeting", "help_request", "thank_you"
    ]
}

PRIORITY_INTENTS = {
    "ride": ["track_ride", "driver_late", "cancel_ride"],
    "payment": ["payment_failed", "refund_status", "payment_issue"],
    "safety": ["safety_issue", "emergency_sos", "driver_misbehavior"]
}

def get_smart_suggestions(intent: str, user_id: int):
    state = get_state(user_id)
    last_intent = state.get("last_intent")

    # If unknown → fallback to last intent context
    target_intent = intent
    if target_intent == "unknown_intent" and last_intent:
        target_intent = last_intent

    for category, intents in INTENT_GROUPS.items():
        if target_intent.lower() in [i.lower() for i in intents]:
            priority = PRIORITY_INTENTS.get(category, intents)
            return [
                {"label": i.replace("_", " ").title(), "intent": i.upper()}
                for i in priority[:3]
            ]

    # Global default suggestions
    return [
        {"label": "Track Ride", "intent": "TRACK_RIDE"},
        {"label": "Payment Issue", "intent": "PAYMENT_FAILED"},
        {"label": "Safety Issue", "intent": "SAFETY_CONCERN"}
    ]

def format_message(template: str, context: dict):
    try:
        return template.format(**context)
    except:
        return template

INTENT_CONFIG = {
    "TRACK_RIDE": {
        "message": "Driver {driver_name} is arriving in {eta}. You can track them live in the app.",
        "actions": ["TRACK_RIDE", "CALL_DRIVER"],
        "show_feedback": True
    },
    "SAFETY_CONCERN": {
        "message": "Your safety is our top priority. Please tell us what happened so we can take immediate action.",
        "next_options": [
            {"label": "Rash Driving", "intent": "RASH_DRIVING"},
            {"label": "Driver Misbehavior", "intent": "DRIVER_MISBEHAVIOR"},
            {"label": "SOS Emergency", "intent": "SOS"}
        ]
    },
    "RASH_DRIVING": {
        "message": "We take rash driving very seriously and will investigate this trip's GPS data.",
        "actions": ["REPORT_DRIVER", "CALL_SUPPORT"]
    },
    "SOS": {
        "message": "🚨 EMERGENCY DETECTED. Our safety team is being alerted. Please stay safe.",
        "actions": ["CALL_SUPPORT"],
        "escalate": True
    },
    "REPORT_DRIVER": {
        "message": "Your complaint has been registered. Our safety team will review this within 24 hours.",
        "actions": ["CALL_SUPPORT"],
        "escalate": True
    },
    "PAYMENT_FAILED": {
        "message": "We noticed your payment failed. This is usually due to an expired card or bank issue.",
        "actions": ["RETRY_PAYMENT", "CALL_SUPPORT"],
        "escalate": True
    },
    "BILLING_ISSUE": {
        "message": "I can help you with your billing concern. Would you like to dispute a charge?",
        "actions": ["CALL_SUPPORT"],
        "show_feedback": True
    },
    "CANCEL_RIDE": {
        "message": "I can help you with your cancellation. Note that cancellation fees may apply depending on how long the driver has been waiting.",
        "actions": ["CANCEL_RIDE"],
        "show_feedback": True
    },
    "ACCOUNT_ISSUE": {
        "message": "For account or login issues, please ensure you are using your registered phone number.",
        "actions": ["CALL_SUPPORT"]
    },
    "TECHNICAL_ISSUE": {
        "message": "We apologize for the technical glitch. Please try restarting the app or check your internet connection.",
        "actions": ["CALL_SUPPORT"]
    },
    "PROMO_ISSUE": {
        "message": "If your promo code isn't working, please check the terms and conditions or expiry date.",
        "actions": ["CALL_SUPPORT"],
        "show_feedback": True
    },
    "GREETING": {
        "message": "Hello! I am your Urban Taxi assistant. How can I help you today?",
        "next_options": [
            {"label": "Track My Ride", "intent": "TRACK_RIDE"},
            {"label": "Payment Issue", "intent": "PAYMENT_FAILED"},
            {"label": "Safety Concern", "intent": "SAFETY_CONCERN"}
        ]
    },
    "REFUND_ISSUE": {
        "message": "Refunds usually take 5-7 business days to flash in your account.",
        "actions": ["CALL_SUPPORT"],
        "escalate": True
    },
    "LOST_ITEM": {
        "message": "If you lost an item, we will try to connect you with your driver immediately.",
        "actions": ["CALL_DRIVER", "CALL_SUPPORT"]
    },
    "GENERAL_HELP": {
        "message": "I can help with rides, payments, and safety. What do you need help with?",
        "next_options": [
            {"label": "Ride Help", "intent": "TRACK_RIDE"},
            {"label": "Payment Help", "intent": "PAYMENT_FAILED"}
        ]
    },
    "UNKNOWN": {
        "message": "I'm not sure I understand. Would you like to speak to a human?",
        "actions": ["CALL_SUPPORT"]
    }
}

def build_response(intent: str, user_id: int = 1):
    # Step 2 — Normalize
    intent = intent.upper().strip().replace(" ", "_")
    
    # Step 5 — Apply Alias
    intent = INTENT_ALIASES.get(intent, intent)
    
    config = INTENT_CONFIG.get(intent, {})
    
    if not config:
        print("WARNING: Intent not found in INTENT_CONFIG:", intent)

    # Step 5 — Action/Escalation Layer
    intent_lower = intent.lower()

    # TRACK_RIDE
    if intent_lower == "track_ride":
        ride = get_active_ride(user_id)
        driver = get_driver(ride["driver_id"])
        return {
            "message": f"{driver['name']} ({driver['rating']}⭐) is {ride['eta_minutes']} mins away. Vehicle: {driver['vehicle']}",
            "next_options": [],
            "actions": [{"type": "CALL_DRIVER"}],
            "show_feedback": True,
            "escalate": False,
            "ticket_ref": None
        }

    # DRIVER_LATE
    if intent_lower == "driver_late":
        return {
            "message": "Your driver is running late. Would you like to call or report?",
            "next_options": [],
            "actions": [{"type": "CALL_DRIVER"}, {"type": "REPORT_DRIVER"}],
            "show_feedback": True,
            "escalate": False,
            "ticket_ref": None
        }

    # PAYMENT_FAILED
    if intent_lower in ["payment_failed", "payment_issue"]:
        payment = get_payment_status(user_id)
        return {
            "message": f"Payment failed: {payment['reason']}. Amount: ₹{payment['amount']}",
            "next_options": [],
            "actions": [{"type": "RETRY_PAYMENT"}],
            "show_feedback": True,
            "escalate": True,
            "ticket_ref": None
        }

    # REFUND_STATUS
    if intent_lower == "refund_status":
        refund = get_refund_status(user_id)
        return {
            "message": f"Refund of ₹{refund['amount']} is {refund['status']}",
            "next_options": [],
            "actions": [],
            "show_feedback": True,
            "escalate": False,
            "ticket_ref": None
        }

    # SAFETY / ISSUE INTENTS
    if intent_lower in ["rash_driving", "driver_misbehavior", "safety_concern", "safety_issue"]:
        issue = create_issue(user_id, intent, "User reported safety issue")
        return {
            "message": "Your complaint has been registered. Our team will take action.",
            "next_options": [],
            "actions": [{"type": "CALL_SUPPORT"}],
            "show_feedback": True,
            "escalate": True,
            "ticket_ref": issue["ticket_ref"]
        }

    ticket_ref = None

    # Mock dynamic context (replace later with real API data)
    # ride_data = get_ride_details(user_id) # This line is removed as per instruction
    dynamic_context = {
        "driver_name": None, # These are now handled by specific intent blocks
        "eta": None,
        "vehicle": None
    }

    message_template = config.get("message", "")
    message = format_message(message_template, dynamic_context)

    if intent_lower in ["unknown", "unknown_intent"]:
        count = increment_fallback(user_id)
        print(f"DEBUG: Unknown intent, fallback_count={count}")

        if count == 1:
            return {
                "message": "I didn’t fully understand. Here are some things I can help with:",
                "next_options": get_smart_suggestions("unknown_intent", user_id),
                "actions": [],
                "show_feedback": False,
                "escalate": False,
                "ticket_ref": None
            }
        
        if count == 2:
            return {
                "message": "I'm still having trouble. Are you looking for help with one of these?",
                "next_options": get_smart_suggestions("unknown_intent", user_id),
                "actions": [{"type": "CALL_SUPPORT"}],
                "show_feedback": False,
                "escalate": False,
                "ticket_ref": None
            }

        # count >= 3
        return {
            "message": "I'm having trouble understanding. Would you like to connect with our support team?",
            "next_options": [],
            "actions": [{"type": "CALL_SUPPORT"}],
            "show_feedback": False,
            "escalate": True,
            "ticket_ref": None
        }

    ticket_ref = None

    if config.get("escalate"):
        ticket = create_ticket(
            issue_type=intent,
            user_id=user_id,
            description=message
        )
        ticket_ref = ticket.ticket_ref

    # Step 6 — Safe Default Response
    return {
        "message": message if config else f"Intent '{intent}' not configured.",
        "next_options": config.get("next_options", []),
        "actions": [{"type": a} for a in config.get("actions", [])],
        "show_feedback": config.get("show_feedback", False),
        "escalate": config.get("escalate", False),
        "ticket_ref": ticket_ref
    }
