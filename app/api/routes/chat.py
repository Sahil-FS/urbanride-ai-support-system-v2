import logging
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse

from app.services.intent_service.service import detect_intent
from app.services.multilingual_service import detect_language_and_intent, get_response as multi_get_response
from app.services.flow_engine import handle_flow
from app.services.action_engine import execute_action
from app.services.chatbot_engine import get_response as chatbot_response
from app.services.chatbot_engine import PILL_INTENT_MAP

logger = logging.getLogger(__name__)
router = APIRouter()

INTENT_ACTION_MAP = {
    "report_driver_contact_issue": "CREATE_TICKET_DRIVER_UNREACHABLE",
    "driver_misbehavior": "CREATE_TICKET_DRIVER_MISBEHAVIOR",
    "double_payment": "CREATE_TICKET_PAYMENT_ISSUE",
    "refund_not_received": "CREATE_TICKET_REFUND_ISSUE",
    "contact_support": "CONTACT_SUPPORT",
}

TICKET_INTENTS = set(INTENT_ACTION_MAP.keys())

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:

    if request.message.startswith("ACTION:"):
        action = request.message.replace("ACTION:", "")
        result = execute_action(action, request.user_id)

        return ChatResponse(
            message=result.get("message", ""),
            next_options=[],
            actions=[],
            show_feedback=False,
            escalate=True,
            ticket_ref=result.get("ticket_ref")
        )

    intent, lang = detect_language_and_intent(request.message)

    if not intent:
        intent, confidence = detect_intent(request.message)
        lang = "en"
        if confidence < 0.4:
            intent = "unknown_intent"
    else:
        confidence = 1.0

    final_intent = handle_flow(request.user_id, intent)

    bot_result = chatbot_response(
        intent=final_intent,
        confidence=confidence,
        original_text=request.message
    )

    resolved_intent = bot_result.get("resolved_intent", final_intent)

    action_result = None
    action_type = INTENT_ACTION_MAP.get(resolved_intent)

    if action_type and resolved_intent in TICKET_INTENTS:
        action_result = execute_action(action_type, request.user_id)

    is_pill = request.message.lower().strip() in [
        key.lower() for key in PILL_INTENT_MAP.keys()
    ]

    if lang != "en" and not is_pill:
        bot_result["response"] = multi_get_response(final_intent, lang)

    final_message = bot_result["response"]

    if action_result:
        final_message += "\n\n" + action_result["message"]

    return ChatResponse(
        message=final_message,
        next_options=[
            {"label": opt, "intent": opt}
            for opt in bot_result["sub_options"]
        ],
        actions=[],
        show_feedback=len(bot_result["sub_options"]) == 0,
        escalate=True if action_result else bot_result["show_call_button"],
        ticket_ref=action_result.get("ticket_ref") if action_result else None
    )