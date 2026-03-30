from app.services.ticket_service import create_ticket

def create_issue(user_id: int, issue_type: str, description: str):
    ticket = create_ticket(
        issue_type=issue_type,
        user_id=user_id,
        description=description
    )
    return {
        "ticket_ref": ticket.ticket_ref
    }
