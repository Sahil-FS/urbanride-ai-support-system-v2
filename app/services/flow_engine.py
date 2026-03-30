from app.services.state_service import get_state, set_state, update_state, clear_state


TERMINAL_INTENTS = {
    "call_support",
    "emergency_sos",
    "report_driver"
}


def handle_flow(user_id: int, intent: str):
    # Update history
    update_state(user_id, intent)

    # Get latest state
    state = get_state(user_id)

    # Ensure required fields exist (SAFE DEFAULTS)
    state.setdefault("step", None)
    state.setdefault("context", {})
    state.setdefault("retry_count", 0)
    state.setdefault("last_intent", None)

    # --------------------------------------------------
    # LOOP PREVENTION (prevents infinite same responses)
    # --------------------------------------------------
    if state["last_intent"] == intent:
        state["retry_count"] += 1
    else:
        state["retry_count"] = 0

    state["last_intent"] = intent

    # If user repeats same thing too much → force escalation
    if state["retry_count"] >= 2:
        clear_state(user_id)
        return "FORCE_ESCALATION"

    # --------------------------------------------------
    # ESCALATION CONTROL
    # --------------------------------------------------
    if intent == "escalate":
        if state.get("step") == "ESCALATED":
            return "ALREADY_ESCALATED"

        state["step"] = "ESCALATED"
        set_state(user_id, state)
        return intent

    # --------------------------------------------------
    # SAFETY FLOW (fixed intent name)
    # --------------------------------------------------
    if intent == "safety_issue":
        state["step"] = "ASK_ISSUE"
        set_state(user_id, state)
        return intent

    # Handle safety sub-flow
    if state.get("step") == "ASK_ISSUE":
        state["context"]["issue_type"] = intent
        state["step"] = "ACTION_STAGE"
        set_state(user_id, state)
        return intent

    # --------------------------------------------------
    # TERMINAL STATES (reset conversation)
    # --------------------------------------------------
    if intent in TERMINAL_INTENTS:
        clear_state(user_id)
        return intent

    return intent