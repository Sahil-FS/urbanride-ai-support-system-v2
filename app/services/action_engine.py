from app.services.driver_service import call_driver
from app.services.payment_service import retry_payment
from app.services.ticket_service import create_ticket

def execute_action(action_type: str, user_id: int):
    # --- EXISTING ACTIONS ---
    if action_type == "CALL_DRIVER":
        return call_driver("DR123")

    if action_type == "RETRY_PAYMENT":
        return retry_payment(user_id)

    # --- NEW TICKETING ACTIONS ---
    if action_type == "CREATE_TICKET_DRIVER_UNREACHABLE":
        ticket, is_new = create_ticket(
            user_id=user_id,
            issue_type="driver_unreachable"
        )
        if not is_new:
            return {
                "message": f"⚠️ This issue is already reported. Our team is working on it. (Ticket: {ticket.ticket_ref})",
                "ticket_ref": ticket.ticket_ref
            }
        return {
            "message": "✅ Your issue has been reported. Our team will investigate.",
            "ticket_ref": ticket.ticket_ref
        }

    if action_type == "CREATE_TICKET_DRIVER_MISBEHAVIOR":
        ticket, is_new = create_ticket(
            user_id=user_id,
            issue_type="driver_misbehavior"
        )
        if not is_new:
            return {
                "message": f"⚠️ This issue is already reported. Our team is working on it. (Ticket: {ticket.ticket_ref})",
                "ticket_ref": ticket.ticket_ref
            }
        return {
            "message": "🚨 Driver complaint registered. Action will be taken.",
            "ticket_ref": ticket.ticket_ref
        }

    if action_type == "CREATE_TICKET_PAYMENT_ISSUE":
        ticket, is_new = create_ticket(
            user_id=user_id,
            issue_type="payment_issue"
        )
        if not is_new:
            return {
                "message": f"⚠️ This issue is already reported. Our team is working on it. (Ticket: {ticket.ticket_ref})",
                "ticket_ref": ticket.ticket_ref
            }
        return {
            "message": "💳 Payment issue registered. Our team will review it.",
            "ticket_ref": ticket.ticket_ref
        }

    if action_type == "CREATE_TICKET_REFUND_ISSUE":
        ticket, is_new = create_ticket(
            user_id=user_id,
            issue_type="refund_not_received"
        )
        if not is_new:
            return {
                "message": f"⚠️ This issue is already reported. Our team is working on it. (Ticket: {ticket.ticket_ref})",
                "ticket_ref": ticket.ticket_ref
            }
        return {
            "message": "💰 Refund issue escalated. You will be contacted shortly.",
            "ticket_ref": ticket.ticket_ref
        }

    if action_type == "CONTACT_SUPPORT":
        ticket, is_new = create_ticket(
            user_id=user_id,
            issue_type="contact_support"
        )
        if not is_new:
            return {
                "message": f"⚠️ You already have an open support request. (Ticket: {ticket.ticket_ref})",
                "ticket_ref": ticket.ticket_ref
            }
        return {
            "message": "📞 Connecting to support. Our team will call you shortly.",
            "ticket_ref": ticket.ticket_ref
        }

    # --- DEFAULT RETURN ---
    return {
        "message": "Action executed successfully"
    }
